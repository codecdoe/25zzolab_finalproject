import streamlit as st
import requests

# API 키 설정
API_KEY = "2f7ff809309654c9d9105c45df3f2a65"

st.title("🏞 오늘 날씨 어때? 뭐 입지?")
address = st.text_input("한국 주소를 입력하세요 (예: 삼청동, 마곡동, 강남구):")

# 추천 정보를 반환하는 함수
def get_recommendations(temp: float, weather: str):
    key = "비" if "rain" in weather.lower() else "맑음"
    data = {
        (0, 7): {
            "옷차림": {
                "맑음": "**두꺼운 외투**, **기모 내의**, **장갑**, **모자**, **머플러** 등 보온에 집중해야 합니다. 기온이 매우 낮기 때문에 히트텍이나 패딩 코트처럼 보온력이 뛰어난 의류를 기본으로 착용하세요. 발은 **양털 양말**과 **부츠**로 따뜻하게 유지하세요.",
                "비": "**방수 외투**, **방수 부츠**, **기모 이너**를 착용하고 **우산**이나 **방수 모자**를 꼭 챙기세요. 비와 찬 공기의 결합은 감기를 유발할 수 있습니다."
            },
            "운동": {"맑음": "실내 체육관 운동 추천", "비": "스트레칭, 요가 중심의 실내 운동"},
            "건강": {"맑음": "보온 유지와 수분 섭취를 챙기세요", "비": "젖은 옷은 바로 갈아입고 난방기 건조 주의"}
        },
        (7, 13): {
            "옷차림": {
                "맑음": "**울 코트**, **니트**, **두툼한 바지**를 중심으로 구성하고, 아침저녁 일교차를 대비해 **겹쳐 입기**가 좋습니다. **머플러**나 **비니**는 체온 유지에 도움을 줍니다.",
                "비": "**트렌치코트**, **긴팔 이너**, **레인부츠**를 착용하고, 활동량이 적은 날은 **히트텍**도 고려하세요."
            },
            "운동": {"맑음": "가벼운 등산이나 조깅", "비": "홈트레이닝 위주"},
            "건강": {"맑음": "일교차 유의, 겹겹이 입기", "비": "습도 높은 날 곰팡이 주의"}
        },
        (13, 19): {
            "옷차림": {
                "맑음": "**맨투맨**, **셔츠**, **얇은 자켓**, **청바지** 등이 적절합니다. 가방에 **얇은 겉옷**을 챙기면 실내외 온도 차에 유리합니다.",
                "비": "**바람막이 자켓**, **방수 신발**, **긴팔 이너** 조합이 실용적입니다."
            },
            "운동": {"맑음": "자전거, 산책 등 야외 활동", "비": "헬스장이나 요가 등 실내 운동"},
            "건강": {"맑음": "알레르기 유발 환경 정리 필요", "비": "습기 조절과 제습기 활용"}
        },
        (19, 25): {
            "옷차림": {
                "맑음": "**반팔 티셔츠**, **얇은 셔츠**, **슬랙스**, **면바지** 등 통기성과 활동성을 모두 고려한 옷차림이 적절합니다. **모자**나 **선크림**도 필요합니다.",
                "비": "**얇은 우비**, **샌들**, **반팔**을 조합하고, 우산은 반드시 챙기세요."
            },
            "운동": {"맑음": "야외 걷기, 자전거 추천", "비": "에어로빅, 스피닝 등 실내 유산소"},
            "건강": {"맑음": "자외선 차단 주의, 수분 섭취", "비": "실내 곰팡이와 음식 보관 주의"}
        },
        (25, 100): {
            "옷차림": {
                "맑음": "**민소매**, **반팔**, **반바지**, **린넨 셔츠** 등 최대한 가볍고 통기성 있는 복장이 필요합니다. **모자**, **선글라스**, **자외선 차단제**는 필수이며, 외출 시간은 낮보다 아침이나 저녁이 적합합니다.",
                "비": "**얇은 반팔** 위에 **레인코트**나 **우비** 착용, 젖어도 괜찮은 **샌들**이 적합합니다."
            },
            "운동": {"맑음": "수분 섭취를 충분히 하며 아침 시간대 운동", "비": "실내 스트레칭 위주, 더위 회피 필요"},
            "건강": {"맑음": "열사병 주의, 냉방 대비 가디건 챙기기", "비": "온도 급변 주의, 장시간 외출 자제"}
        }
    }


    for (low, high), info in data.items():
        if low <= temp < high:
            return {
                "옷차림": info["옷차림"].get(key, "해당 날씨 조건의 옷차림 정보가 없습니다."),
                "운동": info["운동"].get(key, ""),
                "건강": info["건강"].get(key, "")
            }

    return {
        "옷차림": "해당 기온에 대한 정보가 없습니다.",
        "운동": "",
        "건강": ""
    }

def get_coordinates(address):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={address},KR&limit=1&appid={API_KEY}"
    res = requests.get(geo_url).json()
    if not res:
        return None, None
    return res[0]["lat"], res[0]["lon"]

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()
    temp = res["main"]["temp"]
    weather = res["weather"][0]["description"]
    return temp, weather

if address:
    lat, lon = get_coordinates(address)
    if lat is None:
        st.error("❌ 주소를 찾을 수 없습니다. 도로명 주소를 다시 확인해주세요.")
    else:
        temp, weather = get_weather(lat, lon)
        st.success(f"""📍 위치: **{address}**  
🌡 현재 기온: **{temp:.1f}°C**  
🌥 날씨 상태: **{weather}**""")

        recommendation = get_recommendations(temp, weather)

        st.markdown("### 👕 옷차림 추천")
        st.markdown(recommendation["옷차림"])

        st.markdown("### 🏃 운동 추천")
        st.markdown(recommendation["운동"])

        st.markdown("### 💡 건강 조언")
        st.markdown(recommendation["건강"])

        st.image(
            "https://wimg.kyeongin.com/news/legacy/file/201810/20181010000733388_1.jpg",
            caption="기온에 따라 달라지는 계절별 옷차림 예시",
            use_column_width=True
        )
