"""Entry point for the champion data pipeline."""

from ....config.settings import settings
from ...infrastructure.parsers.html_parser import HTMLChampionParser
from ...infrastructure.repositories.csv_repository import CSVChampionRepository
from .champion_pipeline_handler import ChampionPipelineHandler


def main() -> None:
    """Main entry point called by GitHub Actions workflow.

    This is the inbound adapter - it wires up all dependencies
    and delegates to the application service.

    It performs dependency injection by:
    1. Creating concrete infrastructure adapters
    2. Injecting them into the handler
    3. Executing the use case
    """
    parser = HTMLChampionParser()
    repository = CSVChampionRepository(filepath="champions.csv")

    pipeline = ChampionPipelineHandler(
        parser=parser,
        repository=repository,
        source_url=settings.scraping.source_url,
    )

    pipeline.run()


if __name__ == "__main__":
    main()
