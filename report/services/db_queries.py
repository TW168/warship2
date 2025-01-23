# report/services/db_queries.py

from report.models import ScrapedCellSummary 


def get_scraped_cell_summaries(): 
    return ScrapedCellSummary.objects.using('eric').all()

