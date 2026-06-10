package com.example.newsbias.dto;

import jakarta.validation.constraints.NotBlank;

public class ArticleAnalyzeRequest {
    private String url;

    @NotBlank
    private String text;

    public ArticleAnalyzeRequest() {}

    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
}
