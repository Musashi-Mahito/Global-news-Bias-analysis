package com.example.newsbias.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.example.newsbias.dto.ArticleAnalyzeRequest;
import com.example.newsbias.model.Article;
import com.example.newsbias.model.BiasReport;
import com.example.newsbias.model.TimelineItem;
import com.example.newsbias.repository.ArticleRepository;
import com.example.newsbias.repository.BiasReportRepository;
import com.example.newsbias.repository.TimelineItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class ArticleService {

    @Autowired
    private ArticleRepository articleRepository;

    @Autowired
    private BiasReportRepository biasReportRepository;

    @Autowired
    private TimelineItemRepository timelineItemRepository;

    @Autowired
    private ObjectMapper objectMapper;

    @Value("${app.ai-service.url}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public Map<String, Object> analyzeArticle(ArticleAnalyzeRequest request) {
        String endpoint = aiServiceUrl + "/analyze";
        
        // 1. Post analysis request to FastAPI Python service
        ResponseEntity<Map> response = restTemplate.postForEntity(endpoint, request, Map.class);
        Map<String, Object> body = response.getBody();
        
        if (body == null) {
            throw new RuntimeException("Empty response from AI analysis pipeline");
        }

        // Generate a random stable id if not returned, but FastAPI returns a unique pipeline structure.
        // Let's assume FastAPI returns article details
        String articleId = UUID.randomUUID().toString();
        
        // 2. Parse results
        String title = (String) body.getOrDefault("title", "News Analysis");
        String content = (String) body.getOrDefault("content", request.getText());
        String source = (String) body.getOrDefault("source", "Unknown");
        String publishDate = (String) body.getOrDefault("publish_date", "2026-06-10");
        String language = (String) body.getOrDefault("language", "en");

        // Save Article
        Article article = Article.builder()
                .id(articleId)
                .title(title)
                .content(content)
                .source(source)
                .publishDate(publishDate)
                .language(language)
                .build();
        articleRepository.save(article);

        // Save Bias Report Details
        Map<String, Object> biasReportMap = (Map<String, Object>) body.get("biasReport");
        Map<String, Object> consensusReportMap = (Map<String, Object>) body.get("consensusReport");
        Map<String, Object> summariesMap = (Map<String, Object>) body.get("multiPerspectiveSummaries");
        List<Map<String, Object>> timelineList = (List<Map<String, Object>>) body.get("timeline");

        String evidenceJson = "";
        String sharedFactsJson = "";
        String disputedClaimsJson = "";
        String summariesJson = "";

        try {
            if (biasReportMap != null && biasReportMap.get("evidence") != null) {
                evidenceJson = objectMapper.writeValueAsString(biasReportMap.get("evidence"));
            }
            if (consensusReportMap != null) {
                if (consensusReportMap.get("sharedFacts") != null) {
                    sharedFactsJson = objectMapper.writeValueAsString(consensusReportMap.get("sharedFacts"));
                }
                if (consensusReportMap.get("disputedClaims") != null) {
                    disputedClaimsJson = objectMapper.writeValueAsString(consensusReportMap.get("disputedClaims"));
                }
            }
            if (summariesMap != null) {
                summariesJson = objectMapper.writeValueAsString(summariesMap);
            }
        } catch (Exception e) {
            System.err.println("Serialization error: " + e.getMessage());
        }

        BiasReport report = BiasReport.builder()
                .articleId(articleId)
                .biasScore(biasReportMap != null ? (Integer) biasReportMap.get("biasScore") : 50)
                .confidence(biasReportMap != null ? (Integer) biasReportMap.get("confidence") : 85)
                .sentimentBias(biasReportMap != null ? (Integer) biasReportMap.get("sentimentBias") : 50)
                .framingBias(biasReportMap != null ? (Integer) biasReportMap.get("framingBias") : 50)
                .omissionBias(biasReportMap != null ? (Integer) biasReportMap.get("omissionBias") : 50)
                .sentimentExplanation(biasReportMap != null ? (String) biasReportMap.get("sentimentExplanation") : "")
                .framingExplanation(biasReportMap != null ? (String) biasReportMap.get("framingExplanation") : "")
                .omissionExplanation(biasReportMap != null ? (String) biasReportMap.get("omissionExplanation") : "")
                .evidence(evidenceJson)
                .agreementPercent(consensusReportMap != null ? (Integer) consensusReportMap.get("agreementPercent") : 75)
                .contradictionPercent(consensusReportMap != null ? (Integer) consensusReportMap.get("contradictionPercent") : 15)
                .uncertaintyPercent(consensusReportMap != null ? (Integer) consensusReportMap.get("uncertaintyPercent") : 10)
                .sharedFacts(sharedFactsJson)
                .disputedClaims(disputedClaimsJson)
                .multiPerspectiveSummaries(summariesJson)
                .build();
        biasReportRepository.save(report);

        // Save Timeline
        if (timelineList != null) {
            for (Map<String, Object> item : timelineList) {
                TimelineItem timelineItem = TimelineItem.builder()
                        .articleId(articleId)
                        .time((String) item.get("time"))
                        .event((String) item.get("event"))
                        .description((String) item.get("description"))
                        .build();
                timelineItemRepository.save(timelineItem);
            }
        }

        // Return combined results mapping
        Map<String, Object> result = new HashMap<>();
        result.put("articleId", articleId);
        result.put("title", title);
        result.put("source", source);
        result.put("publishDate", publishDate);
        result.put("biasReport", report);
        result.put("timeline", timelineList);
        
        return result;
    }

    public BiasReport getReportByArticleId(String articleId) {
        return biasReportRepository.findByArticleId(articleId)
                .orElseThrow(() -> new NoSuchElementException("No report found for article ID: " + articleId));
    }

    public List<TimelineItem> getTimelineByArticleId(String articleId) {
        return timelineItemRepository.findByArticleId(articleId);
    }

    public Map<String, Object> getEventGraph(String articleId) {
        // Fetch Knowledge Graph directly from FastAPI agent
        String endpoint = aiServiceUrl + "/graph/" + articleId;
        try {
            return restTemplate.getForObject(endpoint, Map.class);
        } catch (Exception e) {
            System.err.println("Error fetching graph from AI service: " + e.getMessage());
            // return a fallback mock graph structure
            Map<String, Object> mockGraph = new HashMap<>();
            mockGraph.put("nodes", List.of());
            mockGraph.put("edges", List.of());
            return mockGraph;
        }
    }
}
