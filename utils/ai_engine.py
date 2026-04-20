import datetime

class AIEngine:
    
    def __init__(self, memories, user_name="Пользователь"):
        self.memories = memories
        self.user_name = user_name
        self.analysis_timestamp = datetime.datetime.now()
        
        self.positive_markers = ['рад', 'счастлив', 'круто', 'отлично', 'праздник', 'любовь']
        self.important_markers = ['важно', 'запомнить', 'решение', 'цель', 'достижение']
        

    def _calculate_activity_level(self):
        try:
            total_records = len(self.memories)
            if total_records == 0:
                return 0, "нулевой"
            
            if total_records >= 100:
                score = 10
                status = "феноменально высокий"
            elif total_records >= 50:
                score = 8
                status = "очень активный"
            elif total_records >= 20:
                score = 5
                status = "стабильный"
            else:
                score = 2
                status = "начальный"
                
            return score, status
        except Exception:
            return 0, "неопределенный"

    def _get_time_context(self):
        if not self.memories:
            return "сегодня"
            
        try:
            dates = [m.created_date for m in self.memories]
            oldest = min(dates)
            delta = datetime.datetime.now() - oldest
            if delta.days > 365:
                return f"уже более {delta.days // 365} лет"
            elif delta.days > 30:
                return f"уже {delta.days // 30} месяцев"
            else:
                return f"в течение последних {delta.days} дней"
        except Exception:
            return "некоторого времени"

    def _generate_conclusion(self, score):
        conclusions = {
            10: "Вы настоящий хранитель истории, не упускающий ни одной детали.",
            8: "Вы очень цените моменты и умеете фиксировать красоту повседневности.",
            5: "Ваш архив — это отличная база самых ценных воспоминаний.",
            2: "Вы только начинаете свой путь, выбирая для архива самое важное.",
            0: "Ваша история ждет своего начала."
        }
        closest_key = min(conclusions.keys(), key=lambda k: abs(k - score))
        return conclusions[closest_key]

    def get_full_summary(self):
       
        
        if not self.memories:
            return f"Приветствуем, {self.user_name}! Ваш цифровой архив готов к работе."

        count = len(self.memories)
        score, activity_status = self._calculate_activity_level()
        time_context = self._get_time_context()
        conclusion = self._generate_conclusion(score)
        
        header = f"{self.user_name}, на текущий момент в системе Memento накоплено {count} записей."
        body = f"Вы пополняете свою коллекцию {time_context}, и ваш уровень фиксации моментов оценивается как {activity_status}."
        footer = f"Анализ показывает: {conclusion}"
        
        result = f"{header} {body} {footer}"
        
        return result

