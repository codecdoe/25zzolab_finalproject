import streamlit as st
import requests

# API 키 설정
API_KEY = "2f7ff809309654c9d9105c45df3f2a65"

# UI 구성
st.title("🏞 날씨 기반 옷차림 · 운동 · 건강 추천기")
address = st.text_input("한국 주소를 입력하세요 (예: 서울특별시 강남구):")

# 시각 이미지 삽입
st.image("https://wimg.kyeongin.com/news/legacy/file/201810/20181010000733388_1.jpg", caption="기온에 따라 달라지는 계절별 옷차림 예시")

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
