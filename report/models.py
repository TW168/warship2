# report/models.py

from django.db import models


class ScrapedCellSummary(models.Model):
    scraped_dt = models.DateTimeField()
    Status = models.CharField(max_length=50)
    Cell_counts = models.IntegerField()

    class Meta:
        db_table = "scraped_cell_summary"

    def __str__(self):
        return f"ID: {self.id}, Scraped Date: {self.scraped_dt}, Status: {self.Status}, Cell Counts: {self.Cell_counts}"


# Use to input the data that are unable to automate
class ReportInput(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the ID field
    date = models.DateField()
    lolita_mtd = models.IntegerField()
    houston_mtd = models.IntegerField()
    remington_mtd = models.IntegerField()

    def __str__(self):
        return (
            f"ID: {self.id}, Date: {self.date}, "
            f"Lolita MTD: {self.lolita_mtd}, Houston MTD: {self.houston_mtd}, "
            f"Remington MTD: {self.remington_mtd}"
        )
