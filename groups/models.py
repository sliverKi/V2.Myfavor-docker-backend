from django.db import models
from common.models import CommonModel

class Groups(models.Model):
    class CompanyChoices(models.TextChoices):
        SmTown="SmTown", "SmTown"
        YG="YG","YG"
        JYP="JYP","JYP"
        HYBE="HYBE","HYBE"
        MBK="MBK","MBK"
        StoneMusic="StoneMusic","StoneMusic"
        CUBE="CUBE","CUBE"
        Mistic="Mistic","Mistic"


    class GirlGroupChoices(models.TextChoices):
        ASEPA="ASEPA", "ASEPA"
        AKMU="AKMU", "AKMU"
        BLACKPINK="BLACKPINK", "BLACKPINK"
        
        ITZY="ITZY", "ITZY"
        
        BILLLIE="BILLLIE", "BILLLIE"
        
        NEWJEANS="NEWJEANS","NEWJEANS"
        LESSERAFIM="LESSERAFIM","LESSERAFIM"

        CELEBFIVE="CELEBFIVE", "CELEBFIVE"
       
        CHOBOM="CHOBOM", "CHOBOM"
        GIDLE="GIDLE", "GIDLE"
        CLASSY="CLASSY", "CLASSY"
        DAVICHI="DAVICHI", "DAVICHI"
        
        FROMIS_9 = "FROMIS_9", "FROMIS_9"

    class BoyGroupChoices(models.TextChoices):
        AB6IX = "AB6IX", "AB6IX"
        AKMU   ="AKMU", "AKMU"
        BTOB = "BTOB", "BTOB"
        BTS= "BTS", "BTS"
        DAY_6 = "DAY_6", "DAY6"
        EXO = "EXO", "EXO"
        HIGH_LIGHT= "HIGH_LIGHT", "HIGH_LIGHT"

    class SoloChoices(models.TextChoices):
        GirlSolo = ("GirlSolo", "GirlSolo")
        BoySolo = ("BoySolo", "BoySolo")

    belong=models.CharField(#소속사
        max_length=40,
        blank=True,
        null=True,
        choices=CompanyChoices.choices,
    )

    Girl_group = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=GirlGroupChoices.choices,
        # validators=[group_name_validate]
    )

    Boy_group = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=BoyGroupChoices.choices,
    )
    group_profile = models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
        #validators=[URLValidator( "유효한 URL을 입력하세요. ")]
    )
    idol_solo = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=SoloChoices.choices,
    )
    idol_name_kr = models.ForeignKey(
        "idols.Idol",
        on_delete=models.SET_NULL,
        null=True,
        default="",
        max_length=100,
        related_name="groups_idol_kr"
    )
    idol_name_en = models.ForeignKey(
        "idols.Idol",
        on_delete=models.SET_NULL,
        default="",
        null=True,
        max_length=100,
        related_name="groups_idol_en"

    )
    def __str__(self)->str:
        return f"{self.idol_name_kr}"

    class Meta:
        verbose_name_plural = "Idols_Group"