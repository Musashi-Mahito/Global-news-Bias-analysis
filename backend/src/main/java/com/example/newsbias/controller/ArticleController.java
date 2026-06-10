package com.example.newsbias.controller;

import com.example.newsbias.dto.ArticleAnalyzeRequest;
import com.example.newsbias.model.BiasReport;
import com.example.newsbias.model.TimelineItem;
import com.example.newsbias.service.ArticleService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping
public class ArticleController {

    @Autowired
    private ArticleService articleService;

    @PostMapping("/article/analyze")
    public ResponseEntity<?> analyzeArticle(@Valid @RequestBody ArticleAnalyzeRequest request) {
        try {
            Map<String, Object> result = articleService.analyzeArticle(request);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("Error running analysis pipeline: " + e.getMessage());
        }
    }

    @GetMapping("/report/{id}")
    public ResponseEntity<?> getReport(@PathVariable("id") String id) {
        try {
            BiasReport report = articleService.getReportByArticleId(id);
            return ResponseEntity.ok(report);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/timeline/{id}")
    public ResponseEntity<List<TimelineItem>> getTimeline(@PathVariable("id") String id) {
        List<TimelineItem> timeline = articleService.getTimelineByArticleId(id);
        return ResponseEntity.ok(timeline);
    }

    @GetMapping("/event/{id}")
    public ResponseEntity<?> getEventGraph(@PathVariable("id") String id) {
        Map<String, Object> graph = articleService.getEventGraph(id);
        return ResponseEntity.ok(graph);
    }
}
