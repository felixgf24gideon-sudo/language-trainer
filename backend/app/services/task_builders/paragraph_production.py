import random
from app.models.task import Task
from app.services.task_builders.base import BaseTaskBuilder

PARAGRAPH_TOPICS = {
    7: [
        "rutinitas pagi kamu",
        "hewan peliharaan impianmu",
        "perjalanan yang paling berkesan",
        "hobi yang kamu nikmati"
    ],
    8: [
        "pentingnya menjaga lingkungan",
        "pengaruh teknologi terhadap kehidupan sehari-hari",
        "budaya atau tradisi yang kamu banggakan",
        "teman atau anggota keluarga yang paling menginspirasimu"
    ],
    9: [
        "tantangan terbesar yang pernah kamu hadapi",
        "pandanganmu tentang pendidikan di masa depan",
        "hubungan antara manusia dan alam",
        "dampak media sosial terhadap remaja"
    ],
    10: [
        "peran bahasa Inggris dalam dunia global",
        "etika penggunaan kecerdasan buatan",
        "bagaimana kamu membayangkan dunia 50 tahun ke depan",
        "hubungan antara budaya dan identitas"
    ]
}

class ParagraphProductionTaskBuilder(BaseTaskBuilder):
    @property
    def task_type(self) -> str:
        return "paragraph_production"

    def build(self) -> Task:
        level_key = min(max(self.level, 7), 10)
        topics = []
        for lvl in range(7, level_key + 1):
            if lvl in PARAGRAPH_TOPICS:
                topics.extend(PARAGRAPH_TOPICS[lvl])
        
        if not topics:
            topics = ["rutinitas pagi kamu"]
        
        topic = random.choice(topics)
        instruction = f"Tulis satu paragraf pendek (3-4 kalimat) dalam bahasa Inggris tentang {topic}."
        
        return Task(
            task_type=self.task_type,
            instruction=instruction,
            level=self.level,
            expected_answer=None,
            context_topic=topic
        )
