package com.example.newsbias.model;

import jakarta.persistence.*;

@Entity
@Table(name = "timeline_items")
public class TimelineItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String articleId;

    private String time;
    private String event;

    @Column(columnDefinition = "TEXT")
    private String description;

    public TimelineItem() {}

    public TimelineItem(String articleId, String time, String event, String description) {
        this.articleId = articleId;
        this.time = time;
        this.event = event;
        this.description = description;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getArticleId() { return articleId; }
    public void setArticleId(String articleId) { this.articleId = articleId; }

    public String getTime() { return time; }
    public void setTime(String time) { this.time = time; }

    public String getEvent() { return event; }
    public void setEvent(String event) { this.event = event; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String articleId;
        private String time;
        private String event;
        private String description;

        public Builder articleId(String articleId) {
            this.articleId = articleId;
            return this;
        }

        public Builder time(String time) {
            this.time = time;
            return this;
        }

        public Builder event(String event) {
            this.event = event;
            return this;
        }

        public Builder description(String description) {
            this.description = description;
            return this;
        }

        public TimelineItem build() {
            return new TimelineItem(articleId, time, event, description);
        }
    }
}
