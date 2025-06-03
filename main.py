import streamlit as st
import requests

# API 키 설정
API_KEY = "2f7ff809309654c9d9105c45df3f2a65"

st.title("🏞 날씨 기반 옷차림 · 운동 · 건강 추천기")
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

'''
import streamlit as st
import requests

# API 키 설정
API_KEY = "2f7ff809309654c9d9105c45df3f2a65"

# UI 구성
st.title("🏞 날씨 기반 옷차림 · 운동 · 건강 추천기")
address = st.text_input("한국 주소를 입력하세요 (예: 삼청동, 마곡동, 강남구):")

# 추천 정보를 반환하는 함수
def get_recommendations(temp: float, weather: str):
    ranges = list(range(4, 29, 3))
    closest = max([r for r in ranges if temp >= r], default=4)
    key = "비" if "rain" in weather.lower() else "맑음"

    data = {
        4: {
            "옷차림": {
                "맑음": "4도는 매우 쌀쌀한 날씨로, 두꺼운 겨울 코트, 니트, 기모 바지, 장갑이 필수입니다. 체온 유지를 위해 모자나 목도리도 착용해주는 것이 좋습니다.",
                "비": "비가 오는 추운 날은 방수 외투, 방한 장갑, 방수 부츠, 따뜻한 이너웨어가 필요합니다."
            },
            "운동": {
                "맑음": "걷기나 가벼운 등산 추천. 보온성을 높인 복장을 착용하세요.",
                "비": "실내 자전거, 실내 요가 등 실내 운동이 좋습니다."
            },
            "건강": {
                "맑음": "호흡기 질환 예방을 위해 마스크 착용과 수분 섭취를 잊지 마세요.",
                "비": "감기 예방을 위해 젖은 옷은 바로 갈아입고, 난방기 사용 시 건조함에 주의하세요."
            }
        },
        10: {
            "옷차림": {
                "맑음": "10도 전후의 날씨에는 후드티나 얇은 코트, 니트가 적당하며, 활동성이 좋으면서도 따뜻함을 유지할 수 있는 복장을 추천합니다.",
                "비": "가벼운 방수 재킷과 긴 바지를 추천하며, 외출 시 방수 신발이 필요합니다."
            },
            "운동": {
                "맑음": "야외 조깅이나 하이킹이 적절합니다. 햇볕이 있다면 체온 유지에 용이합니다.",
                "비": "홈트레이닝, 필라테스 등 무리 없는 실내 운동 추천."
            },
            "건강": {
                "맑음": "건조해지는 계절에는 수분 섭취와 보습이 중요합니다.",
                "비": "젖은 환경에서 면역력이 떨어질 수 있으니 외출 후엔 따뜻한 물로 샤워하세요."
            }
        },
        16: {
            "옷차림": {
                "맑음": "맨투맨이나 얇은 니트, 청바지 등 간절기에 적합한 복장이 좋습니다. 가벼운 자켓은 아침저녁에 유용합니다.",
                "비": "바람막이와 긴팔 셔츠, 방수 신발이 효과적입니다."
            },
            "운동": {
                "맑음": "자전거 타기, 야외 스트레칭 등 적절한 야외 운동 추천.",
                "비": "헬스장 근력 운동, 요가 등 실내 중심 운동이 적절합니다."
            },
            "건강": {
                "맑음": "환절기 알레르기 예방을 위해 외출 후 손씻기와 세안 철저히!",
                "비": "습한 날씨엔 곰팡이 주의, 제습기 사용도 고려해보세요."
            }
        },
        22: {
            "옷차림": {
                "맑음": "반팔 티셔츠, 면바지, 원피스 등 가벼운 옷이 적합하며, 햇볕이 강한 경우 모자나 선크림도 추천합니다.",
                "비": "얇은 우비와 통풍 좋은 신발, 반팔 티셔츠 조합이 적절합니다."
            },
            "운동": {
                "맑음": "야외 걷기, 한강 자전거, 공원 운동 추천.",
                "비": "에어로빅, 실내 스피닝 등 실내 유산소 운동 추천."
            },
            "건강": {
                "맑음": "자외선 지수에 따라 선크림 사용, 냉방기 사용 시 건조 주의.",
                "비": "습한 실내 환경 환기 필수, 음식물 부패 주의하세요."
            }
        },
        28: {
            "옷차림": {
                "맑음": "나시, 반바지, 린넨 소재 옷 등이 적당하며, 자외선 차단제를 꼭 바르고 충분한 수분을 섭취하세요.",
                "비": "얇은 반팔에 레인코트를 착용하고, 젖어도 괜찮은 샌들을 신는 것이 좋습니다."
            },
            "운동": {
                "맑음": "이른 아침 또는 해질 무렵에 가벼운 산책이나 스트레칭 권장.",
                "비": "덥고 습할 땐 수영, 실내 걷기 등이 무리 없는 선택입니다."
            },
            "건강": {
                "맑음": "열사병 예방을 위해 자주 쉬고, 물을 자주 마시세요.",
                "비": "에어컨 환경에서 장시간 있을 경우 체온 유지에 주의하세요."
            }
        }
    }

    selected = data[closest]
    return {
        "옷차림": selected["옷차림"][key],
        "운동": selected["운동"][key],
        "건강": selected["건강"][key]
    }

# 위도, 경도 변환
def get_coordinates(address):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={address},KR&limit=1&appid={API_KEY}"
    res = requests.get(geo_url).json()
    if not res:
        return None, None
    return res[0]["lat"], res[0]["lon"]

# 현재 날씨 정보
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(url).json()
    temp = res["main"]["temp"]
    weather = res["weather"][0]["description"]
    return temp, weather

# 실행
# 실행
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

        # ✅ 마지막에 이미지 출력
        st.image(
            "https://wimg.kyeongin.com/news/legacy/file/201810/20181010000733388_1.jpg",
            caption="기온에 따라 달라지는 계절별 옷차림 예시",
            use_column_width=True
        )
'''
