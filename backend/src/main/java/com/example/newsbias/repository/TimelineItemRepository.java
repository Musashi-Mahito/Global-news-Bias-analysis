package com.example.newsbias.repository;

import com.example.newsbias.model.TimelineItem;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface TimelineItemRepository extends JpaRepository<TimelineItem, Long> {
    List<TimelineItem> findByArticleId(String articleId);
}
