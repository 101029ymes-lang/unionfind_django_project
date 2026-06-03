from django.db import models

class Question(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    DIFFICULTY_CHOICES = [
        (EASY, '易'),
        (MEDIUM, '中'),
        (HARD, '難'),
    ]

    chapter = models.PositiveIntegerField(default=9, verbose_name='章節')
    text = models.TextField(verbose_name='題目')
    explanation = models.TextField(blank=True, verbose_name='解析')
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=MEDIUM,
        verbose_name='難易度'
    )
    is_original = models.BooleanField(default=False, verbose_name='是否為自行設計新題')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '題目'
        verbose_name_plural = '題目'

    def __str__(self):
        return self.text[:40]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='choices',
        on_delete=models.CASCADE,
        verbose_name='題目'
    )
    text = models.CharField(max_length=255, verbose_name='選項內容')
    is_correct = models.BooleanField(default=False, verbose_name='是否為正確答案')

    class Meta:
        verbose_name = '選項'
        verbose_name_plural = '選項'

    def __str__(self):
        return self.text
