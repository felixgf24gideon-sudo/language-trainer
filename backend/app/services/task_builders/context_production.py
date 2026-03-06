import random
from app.models.task import Task
from app.services.task_builders.base import BaseTaskBuilder

CONTEXT_TOPICS = {
    5: [
        ("mengapa kamu belajar bahasa Inggris", "learning English motivation"),
        ("hobimu yang paling kamu sukai", "your favorite hobby"),
        ("rutinitas harianmu", "your daily routine"),
        ("makanan favoritmu", "your favorite food")
    ],
    6: [
        ("pentingnya pendidikan", "importance of education"),
        ("manfaat teknologi", "benefits of technology"),
        ("bagaimana kamu menghabiskan waktu luang", "how you spend free time"),
        ("teman terbaikmu", "your best friend")
    ],
    7: [
        ("dampak media sosial", "impact of social media"),
        ("perubahan iklim", "climate change"),
        ("budaya Indonesia", "Indonesian culture"),
        ("rencanamu di masa depan", "your future plans")
    ],
    8: [
        ("globalisasi dan dampaknya", "globalization and its effects"),
        ("peran teknologi dalam pendidikan", "role of technology in education"),
        ("keberagaman budaya", "cultural diversity"),
        ("tantangan generasi muda", "challenges of the young generation")
    ],
    9: [
        ("hubungan antara bahasa dan budaya", "relationship between language and culture"),
        ("etika dalam penggunaan kecerdasan buatan", "ethics in AI use"),
        ("ketidaksetaraan sosial", "social inequality"),
        ("masa depan energi terbarukan", "future of renewable energy")
    ],
    10: [
        ("implikasi filosofis dari teknologi modern", "philosophical implications of modern technology"),
        ("peran individu dalam mengatasi perubahan iklim", "individual's role in addressing climate change"),
        ("evolusi bahasa di era digital", "evolution of language in the digital age"),
        ("keseimbangan antara tradisi dan modernitas", "balance between tradition and modernity")
    ]
}

class ContextProductionTaskBuilder(BaseTaskBuilder):
    @property
    def task_type(self) -> str:
        return "context_production"

    def build(self) -> Task:
        level_key = min(max(self.level, 5), 10)
        topics = []
        for lvl in range(5, level_key + 1):
            if lvl in CONTEXT_TOPICS:
                topics.extend(CONTEXT_TOPICS[lvl])
        
        if not topics:
            topics = [("mengapa kamu belajar bahasa Inggris", "learning English motivation")]
        
        topic_id, topic_en = random.choice(topics)
        instruction = f"Jelaskan dalam satu kalimat bahasa Inggris tentang {topic_id}."
        
        return Task(
            task_type=self.task_type,
            instruction=instruction,
            level=self.level,
            expected_answer=None,
            context_topic=topic_en
        )
