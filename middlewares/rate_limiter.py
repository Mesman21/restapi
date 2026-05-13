import time
from fastapi import Request, HTTPException
from database import get_redis
from services.auth_service import get_current_user

# Задаємо ліміти: (кількість запитів, період у секундах)
RATE_LIMITS = {
    "anonymous": (2, 60),      # Для анонімного користувача 2 реквести за хвилину [cite: 22]
    "authenticated": (10, 60), # 10 для автентифікованого [cite: 22]
}

async def rate_limit(request: Request):
    r = get_redis()
    
    # Визначаємо, хто робить запит [cite: 24]
    auth_header = request.headers.get("Authorization")
    user_id = None
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            user = await get_current_user(token)
            user_id = user["username"]
        except Exception:
            pass

    # identity буде рівне user_id, інакше хост анонімного користувача [cite: 27, 28]
    identity = user_id or request.client.host 
    
    # Визначення типу обмеження [cite: 29, 30]
    limit_type = "authenticated" if user_id else "anonymous"
    limit, period = RATE_LIMITS[limit_type] # [cite: 32]

    # Значення ключа для відповідного користувача [cite: 35]
    key = f"rate_limit:{identity}" 
    
    # Визначаємо часове вікно [cite: 36]
    now = int(time.time()) # [cite: 37]
    window_start = now - period # [cite: 38]

    # Використовуємо pipeline для виконання кількох команд Redis за раз
    async with r.pipeline(transaction=True) as pipe:
        # 1. Очистити всі застарілі записи, старіші за period 
        pipe.zremrangebyscore(key, min=0, max=window_start) 
        
        # 2. Обраховуємо кількість запитів [cite: 41]
        pipe.zcard(key) 
        
        # 3. Додаємо в кеш дані поточного запиту [cite: 43, 44]
        pipe.zadd(key, {str(now): now}) 
        
        # 4. Задаємо expiration, щоб ключі видалялись після period [cite: 45, 46]
        pipe.expire(key, period) 
        
        # Виконуємо всі команди
        results = await pipe.execute()

    # Результат команди zcard (підрахунок) знаходиться під індексом 1
    request_count = results[1]

    # Порівнюємо request_count з limit [cite: 42]
    if request_count >= limit:
        # Якщо ліміт перевищено райзим HTTPException з кодом 429 [cite: 3, 42]
        raise HTTPException(status_code=429, detail="Too many requests")