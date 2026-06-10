package com.example.newsbias.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "articles")
public class Article {
    @Id
    private String id;

    private String title;

    @Column(columnDefinition = "TEXT")
    private String content;

    private String source;

    private String publishDate;

    private String language;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Article() {}

    public Article(String id, String title, String content, String source, String publishDate, String language) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.source = source;
        this.publishDate = publishDate;
        this.language = language;
        this.createdAt = LocalDateTime.now();
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }

    public String getPublishDate() { return publishDate; }
    public void setPublishDate(String publishDate) { this.publishDate = publishDate; }

    public String getLanguage() { return language; }
    public void setLanguage(String language) { this.language = language; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String id;
        private String title;
        private String content;
        private String source;
        private String publishDate;
        private String language;

        public Builder id(String id) {
            this.id = id;
            return this;
        }

        public Builder title(String title) {
            this.title = title;
            return this;
        }

        public Builder content(String content) {
            this.content = content;
            return this;
        }

        public Builder source(String source) {
            this.source = source;
            return this;
        }

        public Builder publishDate(String publishDate) {
            this.publishDate = publishDate;
            return this;
        }

        public Builder language(String language) {
            this.language = language;
            return this;
        }

        public Article build() {
            return new Article(id, title, content, source, publishDate, language);
        }
    }
}
