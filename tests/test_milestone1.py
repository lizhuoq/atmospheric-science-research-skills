import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MilestoneOneTests(unittest.TestCase):
    def test_demo_skill_has_valid_minimal_frontmatter(self):
        skill = (ROOT / "skills" / "atmospheric-science-research" / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---\n", 2)[1]
        self.assertIn("name: atmospheric-science-research", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertNotIn("TODO", skill)
        schema = json.loads((ROOT / "schemas" / "evidence-record.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_live_literature_workflow_is_primary_and_example_corpus_is_optional(self):
        skill_dir = ROOT / "skills" / "atmospheric-science-research"
        skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        discovery = (skill_dir / "references" / "literature-discovery.md").read_text(encoding="utf-8")
        self.assertIn("lightweight coordinator", skill)
        self.assertIn("optional development and regression-test material", skill)
        self.assertIn("Do not bypass paywalls", discovery)
        self.assertIn("access status", discovery)
        self.assertIn("Crossref", discovery)

    def test_required_behavioral_case_categories_exist(self):
        cases = json.loads((ROOT / "tests" / "evaluation_cases.json").read_text(encoding="utf-8"))
        categories = {case["category"] for case in cases}
        self.assertEqual(categories, {"normal", "incomplete_input", "cross_subfield", "conflict", "invalid_source", "causal_overreach", "incompatible_measurement", "copyright", "citation_hallucination"})
        self.assertTrue(all(case.get("must") for case in cases))

    def test_behavioral_evaluation_passes_frozen_policy_cases(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_behavioral_eval.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads((ROOT / "reports" / "behavioral-evaluation.json").read_text(encoding="utf-8"))
        self.assertEqual(report["passed"], 9)
        self.assertIn("not an LLM accuracy", report["scope"])

    def test_all_skills_have_minimal_frontmatter(self):
        expected = {
            "atmospheric-science-research", "atmospheric-literature-search", "atmospheric-paper-reader",
            "atmospheric-research-design", "atmospheric-statistical-analysis", "atmospheric-claim-audit",
            "atmospheric-manuscript-writer", "atmospheric-data-qc", "atmospheric-figure-analysis",
            "atmospheric-peer-review", "atmospheric-model-experiment", "atmospheric-extremes-attribution",
            "atmospheric-composition-air-quality",
        }
        self.assertEqual(expected, {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")})
        for name in expected:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text.split("---\n", 2)[1])

    def test_complete_skill_suite_contract_and_routing(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_skill_suite.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("validated 13 skills and 15 routing cases", result.stdout)
        stats = (ROOT / "skills" / "atmospheric-statistical-analysis" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("CRPS", stats.split("---\n", 2)[1])
        forecast = (ROOT / "skills" / "atmospheric-statistical-analysis" / "forecast-verification-checks.md").read_text(encoding="utf-8")
        self.assertIn("ensemble-size-adjusted", forecast)
        remote = (ROOT / "skills" / "atmospheric-data-qc" / "remote-sensing-collocation.md").read_text(encoding="utf-8")
        self.assertIn("site-held-out", remote)
        ledger = (ROOT / "skills" / "atmospheric-science-research" / "references" / "workflow-ledger.md").read_text(encoding="utf-8")
        self.assertIn("planned_test", ledger)

    def test_installer_can_install_complete_suite(self):
        installer = ROOT / "scripts" / "install_skill.py"
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(installer), "--platform", "codex", "--scope", "project", "--project-dir", tmp, "--all"], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = list((Path(tmp) / ".agents" / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(installed), 13)

    def test_runtime_knowledge_is_pdf_free_and_review_status_is_honest(self):
        skill = ROOT / "skills" / "atmospheric-science-research"
        self.assertFalse(any(skill.rglob("*.pdf")))
        manifest = json.loads((skill / "references" / "runtime-manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["private_build_corpus_required_at_runtime"])
        self.assertTrue(manifest["network_or_user_provided_papers_required_for_new_topic_review"])
        self.assertIn("not a closed-world knowledge base", manifest["bundled_index_role"])
        entity_rows = [json.loads(line) for line in (skill / "references/entity-evidence.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertGreaterEqual(len(entity_rows), 1000)
        self.assertEqual({r["provenance"]["split"] for r in entity_rows}, {"train"})
        self.assertEqual({r["provenance"]["review_status"] for r in entity_rows}, {"machine_draft"})
        self.assertTrue(all(r["provenance"]["rule_eligible"] is False for r in entity_rows))
        rules = json.loads((skill / "references/method-rules.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(rules), 10)
        self.assertTrue(all(r["sources"] and r["review_status"] in {"machine_draft", "human_checked", "expert_checked"} for r in rules))

    def test_taxonomy_scoring_fails_closed_without_human_gold(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "score_taxonomy_review.py")], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PENDING_HUMAN_REVIEW", result.stdout + result.stderr)

    def test_generated_outputs_are_current(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_milestone1.py"), "--check"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        runtime = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_skill_distribution.py"), "--check"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(runtime.returncode, 0, runtime.stdout + runtime.stderr)

    def test_split_is_complete_disjoint_and_sized(self):
        with (ROOT / "data" / "metadata" / "all_selected.csv").open(encoding="utf-8-sig", newline="") as f:
            source = list(csv.DictReader(f))
        with (ROOT / "data" / "splits" / "paper_splits.csv").open(encoding="utf-8-sig", newline="") as f:
            splits = list(csv.DictReader(f))
        self.assertEqual(len(source), len(splits))
        dois = [r["doi"].lower() for r in splits]
        self.assertEqual(len(dois), len(set(dois)))
        self.assertEqual({r["split"] for r in splits}, {"train", "development", "blind_test"})
        counts = {s: sum(r["split"] == s for r in splits) for s in {"train", "development", "blind_test"}}
        self.assertLessEqual(abs(counts["train"] / len(splits) - .70), .02)
        self.assertLessEqual(abs(counts["development"] / len(splits) - .15), .02)
        self.assertLessEqual(abs(counts["blind_test"] / len(splits) - .15), .02)
        for year in {r["year"] for r in splits}:
            year_rows = [r for r in splits if r["year"] == year]
            if len(year_rows) >= 3:
                self.assertEqual({r["split"] for r in year_rows}, {"train", "development", "blind_test"})
        for journal in {r["journal_rank"] for r in splits}:
            self.assertEqual({r["split"] for r in splits if r["journal_rank"] == journal}, {"train", "development", "blind_test"})

    def test_evidence_validator_accepts_fixture_and_rejects_leakage(self):
        validator = ROOT / "skills" / "atmospheric-science-research" / "scripts" / "validate_evidence.py"
        fixture = ROOT / "skills" / "atmospheric-science-research" / "tests" / "fixtures" / "valid-evidence.jsonl"
        valid = subprocess.run([sys.executable, str(validator), str(fixture)], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        record = json.loads(fixture.read_text(encoding="utf-8"))
        record["provenance"]["split"] = "blind_test"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text(json.dumps(record), encoding="utf-8")
            bad = subprocess.run([sys.executable, str(validator), str(path)], cwd=ROOT, text=True, capture_output=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("leakage policy violation", bad.stdout + bad.stderr)

    def test_query_never_exposes_local_path(self):
        query = ROOT / "skills" / "atmospheric-science-research" / "scripts" / "query_corpus.py"
        result = subprocess.run([sys.executable, str(query), "aerosol", "--limit", "2"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("local_path", result.stdout)
        self.assertNotIn("local_fulltext_available", result.stdout)
        self.assertIsInstance(json.loads(result.stdout), list)

    def test_installed_skill_runs_without_repository_data(self):
        installer = ROOT / "scripts" / "install_skill.py"
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "empty-project"
            project.mkdir()
            installed = subprocess.run([sys.executable, str(installer), "--platform", "codex", "--scope", "project", "--project-dir", str(project)], cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            query = project / ".agents" / "skills" / "atmospheric-science-research" / "scripts" / "query_corpus.py"
            result = subprocess.run([sys.executable, str(query), "aerosol", "--limit", "1"], cwd=project, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(len(json.loads(result.stdout)), 1)

    def test_cross_platform_installer_copies_each_skill(self):
        installer = ROOT / "scripts" / "install_skill.py"
        pairs = [("codex", "atmospheric-science-research", ".agents"), ("claude", "atmospheric-statistical-analysis", ".claude"), ("copilot", "atmospheric-data-qc", ".github")]
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            for platform, skill, top in pairs:
                result = subprocess.run([sys.executable, str(installer), "--platform", platform, "--scope", "project", "--project-dir", str(project), "--skill", skill], cwd=ROOT, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((project / top / "skills" / skill / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
