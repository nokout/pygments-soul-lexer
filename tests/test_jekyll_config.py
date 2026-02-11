"""Tests for Jekyll configuration and GitHub Pages setup."""

from pathlib import Path

import pytest
import yaml


@pytest.fixture
def repo_root():
    """Get the repository root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def docs_dir(repo_root):
    """Get the docs directory."""
    return repo_root / "docs"


@pytest.fixture
def jekyll_config(docs_dir):
    """Load Jekyll configuration."""
    config_path = docs_dir / "_config.yml"
    with open(config_path) as f:
        return yaml.safe_load(f)


class TestJekyllConfiguration:
    """Test Jekyll configuration for GitHub Pages."""

    def test_config_file_exists(self, docs_dir):
        """Test that _config.yml exists in docs directory."""
        config_path = docs_dir / "_config.yml"
        assert config_path.exists(), "Jekyll config file _config.yml not found in docs/"

    def test_config_is_valid_yaml(self, docs_dir):
        """Test that _config.yml is valid YAML."""
        config_path = docs_dir / "_config.yml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        assert isinstance(config, dict), "Jekyll config should be a valid YAML dictionary"

    def test_required_config_fields(self, jekyll_config):
        """Test that required Jekyll configuration fields are present."""
        required_fields = ["title", "description", "theme", "markdown"]
        for field in required_fields:
            assert field in jekyll_config, f"Required field '{field}' missing from Jekyll config"

    def test_baseurl_configured(self, jekyll_config):
        """Test that baseurl is configured for GitHub Pages subpath deployment."""
        assert "baseurl" in jekyll_config, "baseurl is required for GitHub Pages subpath deployment"
        assert jekyll_config["baseurl"] == "/pygments-soul-lexer", (
            "baseurl should be '/pygments-soul-lexer' for correct GitHub Pages URLs"
        )

    def test_url_configured(self, jekyll_config):
        """Test that url is configured for GitHub Pages."""
        assert "url" in jekyll_config, "url is required for GitHub Pages"
        assert jekyll_config["url"] == "https://nokout.github.io", (
            "url should be 'https://nokout.github.io' for GitHub Pages"
        )

    def test_theme_configured(self, jekyll_config):
        """Test that a Jekyll theme is configured."""
        assert "theme" in jekyll_config, "Jekyll theme should be configured"
        assert jekyll_config["theme"] in [
            "jekyll-theme-minimal",
            "jekyll-theme-cayman",
            "jekyll-theme-slate",
            "jekyll-theme-architect",
            "jekyll-theme-tactile",
            "jekyll-theme-dinky",
            "jekyll-theme-modernist",
            "jekyll-theme-leap-day",
            "jekyll-theme-merlot",
            "jekyll-theme-midnight",
            "jekyll-theme-minima",
            "jekyll-theme-time-machine",
            "jekyll-theme-hacker",
        ], f"Theme '{jekyll_config['theme']}' is not a supported GitHub Pages theme"

    def test_markdown_processor(self, jekyll_config):
        """Test that markdown processor is configured."""
        assert "markdown" in jekyll_config, "Markdown processor should be configured"
        assert jekyll_config["markdown"] == "kramdown", (
            "GitHub Pages uses kramdown as the markdown processor"
        )


class TestMarkdownFiles:
    """Test markdown files have proper Jekyll front matter."""

    def test_index_md_exists(self, docs_dir):
        """Test that index.md exists in docs directory."""
        index_path = docs_dir / "index.md"
        assert index_path.exists(), "index.md not found in docs/"

    def test_index_md_has_front_matter(self, docs_dir):
        """Test that index.md has Jekyll front matter."""
        index_path = docs_dir / "index.md"
        with open(index_path) as f:
            content = f.read()
        assert content.startswith("---\n"), "index.md should start with Jekyll front matter (---)"
        lines = content.split("\n")
        # Find the closing --- for front matter
        closing_index = None
        for i in range(1, len(lines)):
            if lines[i] == "---":
                closing_index = i
                break
        assert closing_index is not None, "index.md front matter should have closing ---"
        assert closing_index > 1, "index.md front matter should have content between --- markers"

    def test_index_md_front_matter_has_layout(self, docs_dir):
        """Test that index.md front matter includes layout."""
        index_path = docs_dir / "index.md"
        with open(index_path) as f:
            content = f.read()
        # Extract front matter
        if content.startswith("---\n"):
            parts = content.split("---\n", 2)
            if len(parts) >= 2:
                front_matter = yaml.safe_load(parts[1])
                assert "layout" in front_matter, "index.md front matter should include 'layout'"
                assert front_matter["layout"] == "default", "index.md should use 'default' layout"

    def test_all_markdown_files_have_front_matter(self, docs_dir):
        """Test that all markdown files in docs have Jekyll front matter."""
        md_files = list(docs_dir.glob("*.md"))
        assert len(md_files) > 0, "No markdown files found in docs/"

        for md_file in md_files:
            with open(md_file) as f:
                content = f.read()
            assert content.startswith("---\n"), (
                f"{md_file.name} should start with Jekyll front matter (---)"
            )


class TestDocsStructure:
    """Test docs directory structure for GitHub Pages."""

    def test_docs_directory_exists(self, repo_root):
        """Test that docs directory exists."""
        docs_dir = repo_root / "docs"
        assert docs_dir.exists(), "docs/ directory not found"
        assert docs_dir.is_dir(), "docs/ should be a directory"

    def test_examples_directory_exists(self, docs_dir):
        """Test that examples directory exists in docs."""
        examples_dir = docs_dir / "examples"
        assert examples_dir.exists(), "docs/examples/ directory not found"
        assert examples_dir.is_dir(), "docs/examples/ should be a directory"

    def test_html_examples_exist(self, docs_dir):
        """Test that HTML examples are generated in docs/examples."""
        examples_dir = docs_dir / "examples"
        html_files = list(examples_dir.glob("*.html"))
        assert len(html_files) > 0, "No HTML examples found in docs/examples/"

        # Check for expected example files
        expected_examples = [
            "basic_syntax.html",
            "database_ops.html",
            "oop_features.html",
            "text_blocks.html",
        ]
        existing_files = [f.name for f in html_files]
        for expected in expected_examples:
            assert expected in existing_files, (
                f"Expected example {expected} not found in docs/examples/"
            )


class TestGitHubPagesDeployment:
    """Test GitHub Pages deployment configuration."""

    def test_deploy_workflow_exists(self, repo_root):
        """Test that GitHub Pages deploy workflow exists."""
        workflow_path = repo_root / ".github" / "workflows" / "deploy-pages.yml"
        assert workflow_path.exists(), "deploy-pages.yml workflow not found"

    def test_deploy_workflow_valid_yaml(self, repo_root):
        """Test that deploy workflow is valid YAML."""
        workflow_path = repo_root / ".github" / "workflows" / "deploy-pages.yml"
        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)
        assert isinstance(workflow, dict), "deploy-pages.yml should be valid YAML"

    def test_deploy_workflow_uploads_docs(self, repo_root):
        """Test that deploy workflow uploads docs directory."""
        workflow_path = repo_root / ".github" / "workflows" / "deploy-pages.yml"
        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)

        # Check that workflow has jobs
        assert "jobs" in workflow, "Workflow should have jobs defined"

        # Find the upload artifact step
        found_docs_upload = False
        for _job_name, job_config in workflow["jobs"].items():
            if "steps" in job_config:
                for step in job_config["steps"]:
                    # Check for upload-pages-artifact action with docs path
                    if (
                        "uses" in step
                        and "upload-pages-artifact" in step["uses"]
                        and "with" in step
                        and "path" in step["with"]
                        and "docs" in step["with"]["path"]
                    ):
                        found_docs_upload = True
                        break
            if found_docs_upload:
                break

        assert found_docs_upload, "Deploy workflow should upload docs/ directory"

    def test_deploy_workflow_generates_examples(self, repo_root):
        """Test that deploy workflow generates HTML examples."""
        workflow_path = repo_root / ".github" / "workflows" / "deploy-pages.yml"
        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)

        # Check for step that generates examples
        found_generate_step = False
        for _job_name, job_config in workflow["jobs"].items():
            if "steps" in job_config:
                for step in job_config["steps"]:
                    # Check step name or run command for example generation
                    if "name" in step and "example" in step["name"].lower():
                        found_generate_step = True
                        break
                    if "run" in step and (
                        "generate_examples" in step["run"] or "pygmentize" in step["run"]
                    ):
                        found_generate_step = True
                        break
            if found_generate_step:
                break

        assert found_generate_step, "Deploy workflow should generate HTML examples"

    def test_deploy_workflow_copies_readme(self, repo_root):
        """Test that deploy workflow copies README to docs."""
        workflow_path = repo_root / ".github" / "workflows" / "deploy-pages.yml"
        with open(workflow_path) as f:
            workflow = yaml.safe_load(f)

        # Check for step that copies README
        found_copy_step = False
        for _job_name, job_config in workflow["jobs"].items():
            if "steps" in job_config:
                for step in job_config["steps"]:
                    # Check step name or run command for README copying
                    if "name" in step and "readme" in step["name"].lower():
                        found_copy_step = True
                        break
                    if "run" in step and ("copy_readme" in step["run"] or "README" in step["run"]):
                        found_copy_step = True
                        break
            if found_copy_step:
                break

        assert found_copy_step, "Deploy workflow should copy README to docs"
