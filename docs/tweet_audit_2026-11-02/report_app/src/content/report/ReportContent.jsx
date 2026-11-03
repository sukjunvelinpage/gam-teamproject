import React from "react";
import { DataComponent, DataTable, ReportSection, RichNarrative, useDataApp } from "../../data-app-public.jsx";
import content from "./audit-content.json";

export function ReportContent() {
  const { appTitle, canEdit, mode, setAppTitle, reviewedRows, visible } = useDataApp();
  const auditRows = reviewedRows("audit");
  return <article className="report-content tweet-audit-report" aria-label="트럼프 트윗 분류와 누락 감사 보고서">
    <header className="report-hero">
      <h1 data-data-app-title contentEditable={canEdit && mode === "edit"} suppressContentEditableWarning
        onBlur={canEdit && mode === "edit" ? (event) => setAppTitle(event.currentTarget.textContent?.trim() || appTitle) : undefined}>
        {appTitle}
      </h1>
      <RichNarrative id="audit-byline" value="GAM 팀프로젝트 · 감사일 2026-11-02 · 원본을 보존한 검토" label="보고서 부제 편집" />
    </header>
    {content.map((block) => {
      if (!visible(block.id)) return null;
      if (block.kind === "table") {
        const rows = reviewedRows(block.queryId);
        return <DataComponent key={block.id} id={block.id} title={block.title} queryId={block.queryId}
          kind="table" displayRows={rows} sourceRows={rows}>
          <h3 className="audit-table-heading">{block.title}</h3>
          <DataTable columns={block.columns} rows={rows} caption={block.title} searchable={false} />
        </DataComponent>;
      }
      return <ReportSection key={block.id} id={block.id} title={block.text.split("\n")[0].replace(/^#+\s*/, "")}
        queryId="audit" sourceRows={auditRows} showHeading={false}>
        <RichNarrative id={`${block.id}:body`} value={block.text} label="감사 보고서 본문 편집" />
      </ReportSection>;
    })}
  </article>;
}
