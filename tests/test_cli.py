"""Tests for erd_index.cli — argument parsing and subcommand dispatch.

Pipeline functions are mocked so tests validate CLI wiring only.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from erd_index.cli import build_parser, main

# load_settings is lazily imported inside main(), so we patch it at its source.
_PATCH_LOAD = "erd_index.settings.load_settings"


# ===================================================================
# Argument parsing
# ===================================================================


class TestBuildParser:
    """build_parser returns an argparse.ArgumentParser with all subcommands."""

    def test_sync_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sync"])
        assert args.command == "sync"
        assert args.full_rebuild is False
        assert args.dry_run is False

    def test_sync_full_rebuild(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sync", "--full-rebuild"])
        assert args.full_rebuild is True

    def test_sync_dry_run(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sync", "--dry-run"])
        assert args.dry_run is True

    def test_ingest_md_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-md"])
        assert args.command == "ingest-md"
        assert args.changed_only is False
        assert args.dry_run is False
        assert args.source_name is None

    def test_ingest_md_changed_only(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-md", "--changed-only"])
        assert args.changed_only is True

    def test_ingest_md_source_name(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-md", "--source-name", "ethresearch"])
        assert args.source_name == "ethresearch"

    def test_ingest_md_dry_run(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-md", "--dry-run"])
        assert args.dry_run is True

    def test_ingest_code_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-code"])
        assert args.command == "ingest-code"
        assert args.repo is None
        assert args.changed_only is False
        assert args.dry_run is False
        assert args.max_files == 0

    def test_ingest_code_repo(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-code", "--repo", "geth"])
        assert args.repo == "geth"

    def test_ingest_code_max_files(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-code", "--max-files", "50"])
        assert args.max_files == 50

    def test_build_graph_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["build-graph"])
        assert args.command == "build-graph"
        assert args.changed_only is False

    def test_build_graph_changed_only(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["build-graph", "--changed-only"])
        assert args.changed_only is True

    def test_link_specs_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["link-specs"])
        assert args.command == "link-specs"

    def test_stats_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["stats"])
        assert args.command == "stats"

    def test_stats_repo_filter(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["stats", "--repo", "lighthouse"])
        assert args.repo == "lighthouse"

    def test_init_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["init"])
        assert args.command == "init"


class TestVerboseFlag:
    """The -v / --verbose flag propagates correctly."""

    def test_verbose_on_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sync", "-v"])
        assert args.verbose is True

    def test_verbose_defaults_to_false(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sync"])
        assert args.verbose is False

    def test_verbose_long_form_on_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest-md", "--verbose"])
        assert args.verbose is True

    def test_verbose_on_init_uses_main_parser(self) -> None:
        """init has no verbose_parent, so -v must be placed before subcommand."""
        parser = build_parser()
        args = parser.parse_args(["-v", "init"])
        assert args.verbose is True

    def test_verbose_on_different_subcommands(self) -> None:
        """Several subcommands accept -v via the verbose_parent."""
        parser = build_parser()
        for cmd in ("ingest-md", "ingest-code", "build-graph", "link-specs", "sync"):
            args = parser.parse_args([cmd, "-v"])
            assert args.verbose is True, f"-v should work on {cmd}"


class TestBatchSizeFlag:
    """--batch-size overrides the config default."""

    def test_batch_size_default_is_zero(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["sync"])
        assert args.batch_size == 0

    def test_batch_size_override(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--batch-size", "500", "sync"])
        assert args.batch_size == 500


# ===================================================================
# CLI entry point dispatch
# ===================================================================


class TestMainDispatch:
    """main() dispatches to the correct subcommand handler."""

    @patch("erd_index.cli._cmd_sync")
    @patch(_PATCH_LOAD)
    def test_sync_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["sync"])
        mock_cmd.assert_called_once()

    @patch("erd_index.cli._cmd_ingest_md")
    @patch(_PATCH_LOAD)
    def test_ingest_md_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["ingest-md"])
        mock_cmd.assert_called_once()

    @patch("erd_index.cli._cmd_ingest_code")
    @patch(_PATCH_LOAD)
    def test_ingest_code_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["ingest-code"])
        mock_cmd.assert_called_once()

    @patch("erd_index.cli._cmd_build_graph")
    @patch(_PATCH_LOAD)
    def test_build_graph_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["build-graph"])
        mock_cmd.assert_called_once()

    @patch("erd_index.cli._cmd_link_specs")
    @patch(_PATCH_LOAD)
    def test_link_specs_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["link-specs"])
        mock_cmd.assert_called_once()

    @patch("erd_index.cli._cmd_stats")
    @patch(_PATCH_LOAD)
    def test_stats_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["stats"])
        mock_cmd.assert_called_once()

    @patch("erd_index.cli._cmd_init")
    @patch(_PATCH_LOAD)
    def test_init_dispatches(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        mock_load.return_value = MagicMock()
        main(["init"])
        mock_cmd.assert_called_once()

    def test_no_command_exits(self) -> None:
        """No subcommand should print help and exit with code 1."""
        with pytest.raises(SystemExit, match="1"):
            main([])

    @patch("erd_index.cli._cmd_sync")
    @patch(_PATCH_LOAD)
    def test_batch_size_applied_to_settings(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        settings = MagicMock()
        settings.meili = MagicMock(batch_size=1000)
        mock_load.return_value = settings

        main(["--batch-size", "250", "sync"])

        assert settings.meili.batch_size == 250

    @patch("erd_index.cli._cmd_sync")
    @patch(_PATCH_LOAD)
    def test_batch_size_zero_not_applied(
        self, mock_load: MagicMock, mock_cmd: MagicMock,
    ) -> None:
        """batch_size=0 (default) should NOT override the config value."""
        settings = MagicMock()
        settings.meili = MagicMock(batch_size=1000)
        mock_load.return_value = settings

        main(["sync"])

        # batch_size should remain 1000 (not overridden)
        assert settings.meili.batch_size == 1000


# ===================================================================
# Subcommand handler wiring
# ===================================================================


class TestSubcommandHandlers:
    """Subcommand handlers call the correct pipeline functions with correct args."""

    @patch(_PATCH_LOAD)
    def test_ingest_md_passes_flags(self, mock_load: MagicMock) -> None:
        mock_load.return_value = MagicMock()

        with patch("erd_index.pipeline.ingest_markdown") as mock_fn:
            main(["ingest-md", "--changed-only", "--dry-run", "--source-name", "eips"])

        mock_fn.assert_called_once()
        call_kwargs = mock_fn.call_args
        assert call_kwargs.kwargs["changed_only"] is True
        assert call_kwargs.kwargs["dry_run"] is True
        assert call_kwargs.kwargs["source_name"] == "eips"

    @patch(_PATCH_LOAD)
    def test_ingest_code_passes_flags(self, mock_load: MagicMock) -> None:
        mock_load.return_value = MagicMock()

        with patch("erd_index.pipeline.ingest_code") as mock_fn:
            main(["ingest-code", "--repo", "geth", "--changed-only", "--max-files", "10"])

        mock_fn.assert_called_once()
        call_kwargs = mock_fn.call_args
        assert call_kwargs.kwargs["repo_name"] == "geth"
        assert call_kwargs.kwargs["changed_only"] is True
        assert call_kwargs.kwargs["max_files"] == 10

    @patch(_PATCH_LOAD)
    def test_sync_passes_full_rebuild(self, mock_load: MagicMock) -> None:
        mock_load.return_value = MagicMock()

        with patch("erd_index.pipeline.sync_all") as mock_fn:
            main(["sync", "--full-rebuild"])

        mock_fn.assert_called_once()
        call_kwargs = mock_fn.call_args
        # --full-rebuild => changed_only=False
        assert call_kwargs.kwargs["changed_only"] is False

    @patch(_PATCH_LOAD)
    def test_sync_default_changed_only(self, mock_load: MagicMock) -> None:
        mock_load.return_value = MagicMock()

        with patch("erd_index.pipeline.sync_all") as mock_fn:
            main(["sync"])

        mock_fn.assert_called_once()
        call_kwargs = mock_fn.call_args
        # Default (no --full-rebuild) => changed_only=True
        assert call_kwargs.kwargs["changed_only"] is True
