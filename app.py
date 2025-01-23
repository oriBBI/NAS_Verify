import streamlit as st
import pandas as pd
import func  # te.py에서 verify_stock 함수를 가져옵니다.
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")
warnings.filterwarnings("ignore", message="missing ScriptRunContext")


# Streamlit UI
def main():

    # 제목
    st.title("나스닥 필터링 도구")

    # 1행: 필터 조건 버튼
    st.subheader("필터 조건 선택")

    # 열 나누기
    col1, col2, col3, col4, col5 = st.columns(5)

    filter_dict = {'ROE':False, 'PBR': False, 'Revenue': False, 'Net_income':False, 'price_52':False}

    with col1:
        filter_dict['ROE'] = st.checkbox("ROE 증가")
    with col2:
        filter_dict['PBR'] = st.checkbox("PBR 증가")
    with col3:
        filter_dict['Net_income'] = st.checkbox("순이익 증가")
    with col4:
        filter_dict['Revenue'] = st.checkbox("매출 증가")
    with col5:
        filter_dict['price_52'] = st.checkbox("52주 가격 중간값 이하")

    # 2행: 기간 선택
    st.subheader("기간 선택")
    period = st.radio("기간을 선택하세요:", ("2y", "5y", "10y", "Max"), horizontal=True)
    st.write('주식 시간 데이터와 기간이 맞지 않는 경우 자동으로 MAX로 지정합니다.')

    # 3행: 필터링 시작 버튼
    st.subheader("필터링 시작")
    if st.button("필터링 시작"):
        st.success("필터링을 시작합니다! 시간이 걸립니다.")


       #필터링 시작 
        df = pd.read_csv('USSTOCK.csv', encoding = 'cp949')
        tickers = df['Symbol'].dropna().tolist()

        # verify_stock 함수 실행 및 True인 티커 필터링
        valid_tickers = pd.DataFrame()
        trash = pd.DataFrame(columns=['Symbol'])
        ticker_class = {}

        # 진행률 막대 및 진행 상황 페이지에 표시
        progress_bar = st.progress(0)
        progress_text = st.empty()  


        for idx, ticker in enumerate(tickers):
            progress_percentage = (idx + 1) / len(tickers)
            progress_text.write(f'{round(progress_percentage * 100, 2)}% {ticker} 검증 시작')
            progress_bar.progress(progress_percentage)
            
            try:
                stock = func.stock_invest(ticker)
                result  = stock.verify_stock(filter_dict, 0.1, period)
                if result:
                    ticker_class[ticker] = stock
                    df = pd.DataFrame(result, index=[ticker])
                    valid_tickers = pd.concat([valid_tickers, df], axis = 0,ignore_index=False)
                    st.write(f'{ticker} 검증 성공')
                    with st.container():  # 각 종목마다 컨테이너를 사용
                        st.subheader(f'{ticker} Financial Data')
                        col1, col2, col3, col4 = st.columns(4)  # 한 행에 4개의 열로 나누기
                        with col1:
                            st.write('PBR_graph')
                            fig, ax = plt.subplots(figsize=(60,40))
                            stock.PBR_graph(True, ax=ax)  # PBR 그래프 그리기
                            st.pyplot(fig)  # Streamlit에 그래프 표시
                        
                        with col2:
                            st.write('ROE_graph')
                            fig, ax = plt.subplots(figsize=(60,40))
                            stock.ROE_graph(True, ax=ax)  # ROE 그래프 그리기
                            st.pyplot(fig)  # Streamlit에 그래프 표시
                        
                        with col3:
                            st.write('Revenue_Net_income_graph')
                            fig, ax = plt.subplots(figsize=(60,40))
                            stock.Revenue_Net_income_graph(True, ax=ax)  # Revenue & Net Income 그래프 그리기
                            st.pyplot(fig)  # Streamlit에 그래프 표시
                        
                        with col4:
                            st.write('price_52_graph')
                            fig, ax = plt.subplots(figsize=(60,40))
                            stock.price_52_graph(True, ax=ax)  # Revenue & Net Income 그래프 그리기
                            st.pyplot(fig)  # Streamlit에 그래프 표시
                else:
                    trash_ticker = pd.DataFrame(ticker, columns=['Symbol'], index = [0])
                    trash = pd.concat([trash, trash_ticker], axis=0, ignore_index=False)
                    trash.to_csv('trash.csv')
            except Exception as e:
                print('오류', e, end=' ')
                trash_ticker = pd.DataFrame(ticker, columns=['Symbol'], index = [0])
                trash = pd.concat([trash, trash_ticker], axis=0, ignore_index=False)
                trash.to_csv('trash.csv')

if __name__ == '__main__':
    main()

