package com.example.newsbias.model;

import jakarta.persistence.*;

@Entity
@Table(name = "bias_reports")
public class BiasReport {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String articleId;

    private Integer biasScore;
    private Integer confidence;
    private Integer sentimentBias;
    private Integer framingBias;
    private Integer omissionBias;

    @Column(columnDefinition = "TEXT")
    private String sentimentExplanation;

    @Column(columnDefinition = "TEXT")
    private String framingExplanation;

    @Column(columnDefinition = "TEXT")
    private String omissionExplanation;

    @Column(columnDefinition = "TEXT")
    private String evidence;

    private Integer agreementPercent;
    private Integer contradictionPercent;
    private Integer uncertaintyPercent;

    @Column(columnDefinition = "TEXT")
    private String sharedFacts;

    @Column(columnDefinition = "TEXT")
    private String disputedClaims;

    @Column(columnDefinition = "TEXT")
    private String multiPerspectiveSummaries;

    public BiasReport() {}

    public BiasReport(String articleId, Integer biasScore, Integer confidence, Integer sentimentBias,
                      Integer framingBias, Integer omissionBias, String sentimentExplanation,
                      String framingExplanation, String omissionExplanation, String evidence,
                      Integer agreementPercent, Integer contradictionPercent, Integer uncertaintyPercent,
                      String sharedFacts, String disputedClaims, String multiPerspectiveSummaries) {
        this.articleId = articleId;
        this.biasScore = biasScore;
        this.confidence = confidence;
        this.sentimentBias = sentimentBias;
        this.framingBias = framingBias;
        this.omissionBias = omissionBias;
        this.sentimentExplanation = sentimentExplanation;
        this.framingExplanation = framingExplanation;
        this.omissionExplanation = omissionExplanation;
        this.evidence = evidence;
        this.agreementPercent = agreementPercent;
        this.contradictionPercent = contradictionPercent;
        this.uncertaintyPercent = uncertaintyPercent;
        this.sharedFacts = sharedFacts;
        this.disputedClaims = disputedClaims;
        this.multiPerspectiveSummaries = multiPerspectiveSummaries;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getArticleId() { return articleId; }
    public void setArticleId(String articleId) { this.articleId = articleId; }

    public Integer getBiasScore() { return biasScore; }
    public void setBiasScore(Integer biasScore) { this.biasScore = biasScore; }

    public Integer getConfidence() { return confidence; }
    public void setConfidence(Integer confidence) { this.confidence = confidence; }

    public Integer getSentimentBias() { return sentimentBias; }
    public void setSentimentBias(Integer sentimentBias) { this.sentimentBias = sentimentBias; }

    public Integer getFramingBias() { return framingBias; }
    public void setFramingBias(Integer framingBias) { this.framingBias = framingBias; }

    public Integer getOmissionBias() { return omissionBias; }
    public void setOmissionBias(Integer omissionBias) { this.omissionBias = omissionBias; }

    public String getSentimentExplanation() { return sentimentExplanation; }
    public void setSentimentExplanation(String sentimentExplanation) { this.sentimentExplanation = sentimentExplanation; }

    public String getFramingExplanation() { return framingExplanation; }
    public void setFramingExplanation(String framingExplanation) { this.framingExplanation = framingExplanation; }

    public String getOmissionExplanation() { return omissionExplanation; }
    public void setOmissionExplanation(String omissionExplanation) { this.omissionExplanation = omissionExplanation; }

    public String getEvidence() { return evidence; }
    public void setEvidence(String evidence) { this.evidence = evidence; }

    public Integer getAgreementPercent() { return agreementPercent; }
    public void setAgreementPercent(Integer agreementPercent) { this.agreementPercent = agreementPercent; }

    public Integer getContradictionPercent() { return contradictionPercent; }
    public void setContradictionPercent(Integer contradictionPercent) { this.contradictionPercent = contradictionPercent; }

    public Integer getUncertaintyPercent() { return uncertaintyPercent; }
    public void setUncertaintyPercent(Integer uncertaintyPercent) { this.uncertaintyPercent = uncertaintyPercent; }

    public String getSharedFacts() { return sharedFacts; }
    public void setSharedFacts(String sharedFacts) { this.sharedFacts = sharedFacts; }

    public String getDisputedClaims() { return disputedClaims; }
    public void setDisputedClaims(String disputedClaims) { this.disputedClaims = disputedClaims; }

    public String getMultiPerspectiveSummaries() { return multiPerspectiveSummaries; }
    public void setMultiPerspectiveSummaries(String multiPerspectiveSummaries) { this.multiPerspectiveSummaries = multiPerspectiveSummaries; }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String articleId;
        private Integer biasScore;
        private Integer confidence;
        private Integer sentimentBias;
        private Integer framingBias;
        private Integer omissionBias;
        private String sentimentExplanation;
        private String framingExplanation;
        private String omissionExplanation;
        private String evidence;
        private Integer agreementPercent;
        private Integer contradictionPercent;
        private Integer uncertaintyPercent;
        private String sharedFacts;
        private String disputedClaims;
        private String multiPerspectiveSummaries;

        public Builder articleId(String articleId) { this.articleId = articleId; return this; }
        public Builder biasScore(Integer biasScore) { this.biasScore = biasScore; return this; }
        public Builder confidence(Integer confidence) { this.confidence = confidence; return this; }
        public Builder sentimentBias(Integer sentimentBias) { this.sentimentBias = sentimentBias; return this; }
        public Builder framingBias(Integer framingBias) { this.framingBias = framingBias; return this; }
        public Builder omissionBias(Integer omissionBias) { this.omissionBias = omissionBias; return this; }
        public Builder sentimentExplanation(String sentimentExplanation) { this.sentimentExplanation = sentimentExplanation; return this; }
        public Builder framingExplanation(String framingExplanation) { this.framingExplanation = framingExplanation; return this; }
        public Builder omissionExplanation(String omissionExplanation) { this.omissionExplanation = omissionExplanation; return this; }
        public Builder evidence(String evidence) { this.evidence = evidence; return this; }
        public Builder agreementPercent(Integer agreementPercent) { this.agreementPercent = agreementPercent; return this; }
        public Builder contradictionPercent(Integer contradictionPercent) { this.contradictionPercent = contradictionPercent; return this; }
        public Builder uncertaintyPercent(Integer uncertaintyPercent) { this.uncertaintyPercent = uncertaintyPercent; return this; }
        public Builder sharedFacts(String sharedFacts) { this.sharedFacts = sharedFacts; return this; }
        public Builder disputedClaims(String disputedClaims) { this.disputedClaims = disputedClaims; return this; }
        public Builder multiPerspectiveSummaries(String multiPerspectiveSummaries) { this.multiPerspectiveSummaries = multiPerspectiveSummaries; return this; }

        public BiasReport build() {
            return new BiasReport(articleId, biasScore, confidence, sentimentBias, framingBias, omissionBias,
                    sentimentExplanation, framingExplanation, omissionExplanation, evidence, agreementPercent,
                    contradictionPercent, uncertaintyPercent, sharedFacts, disputedClaims, multiPerspectiveSummaries);
        }
    }
}
