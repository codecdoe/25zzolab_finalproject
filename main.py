
import streamlit as st
import requests

# 🔑 OpenWeatherMap API 키
API_KEY = "2f7ff809309654c9d9105c45df3f2a65"

# 👉 페이지 제목
st.title("👕 날씨 기반 옷차림 추천기")
address = st.text_input("한국 주소를 입력하세요 (예: 삼청동, 마곡동):")

# 🧥 기온과 날씨별 옷차림 추천
def get_outfit(temp: float, weather: str):
    ranges = list(range(4, 29, 3))  # 4~28도, 3도 단위
    closest = max([r for r in ranges if temp >= r], default=4)

    outfit_table = {
        4: {"맑음": "두꺼운 코트, 니트, 기모 바지, 장갑", "비": "두꺼운 방수 외투, 방수 부츠, 우산"},
        7: {"맑음": "울 코트, 니트, 청바지, 머플러", "비": "방수 트렌치코트, 긴팔, 레인부츠"},
        10: {"맑음": "가벼운 코트, 후드티, 기모바지", "비": "얇은 우비, 니트, 운동화"},
        13: {"맑음": "자켓, 가디건, 긴팔 티셔츠", "비": "얇은 아우터, 긴팔, 방수 신발"},
        16: {"맑음": "맨투맨, 가벼운 니트, 청바지", "비": "바람막이, 긴팔, 우산"},
        19: {"맑음": "긴팔 티셔츠, 슬랙스, 셔츠", "비": "얇은 셔츠, 방수 신발, 우산"},
        22: {"맑음": "반팔 티셔츠, 면바지, 원피스", "비": "반팔 + 우비, 샌들"},
        25: {"맑음": "민소매, 반바지, 얇은 셔츠", "비": "얇은 반팔, 통풍 좋은 신발"},
        28: {"맑음": "나시, 반팔, 린넨 바지, 선글라스", "비": "얇은 옷, 가벼운 우산, 슬리퍼"}
    }

    key = "비" if "rain" in weather.lower() else "맑음"
    return outfit_table[closest][key]

# 📍 주소 → 위도/경도 변환
def get_coordinates(address):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={address},KR&limit=1&appid={API_KEY}"
    res = requests.get(geo_url).json()
    if not res:
        return None, None
    return res[0]["lat"], res[0]["lon"]

# 🌤 현재 날씨 가져오기
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()
    temp = res["main"]["temp"]
    weather = res["weather"][0]["description"]
    return temp, weather

# 🚀 실행
if address:
    lat, lon = get_coordinates(address)
    if lat is None:
        st.error("❌ 주소를 찾을 수 없습니다. 다시 확인해주세요.")
    else:
        temp, weather = get_weather(lat, lon)
        st.success(f"📍 '{address}'의 현재 기온은 **{temp:.1f}°C**, 날씨는 '**{weather}**'입니다.")
        outfit = get_outfit(temp, weather)
        st.markdown(f"👚 **추천 옷차림:** {outfit}")
