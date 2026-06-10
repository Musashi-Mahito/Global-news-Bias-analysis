package com.example.newsbias.repository;

import com.example.newsbias.model.BiasReport;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface BiasReportRepository extends JpaRepository<BiasReport, Long> {
    Optional<BiasReport> findByArticleId(String articleId);
}
