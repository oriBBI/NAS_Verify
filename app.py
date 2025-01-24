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


    filter_dict = {'ROE':False, 'PBR': False, 'Revenue': False, 'Net_income':False, 'price_52':False, 'D_E':False, 'D_A':False, 'I_C':False, 'D_EB':False }
    # 1행: 필터 조건 버튼
    st.subheader("필터 조건 선택")

    st.subheader("재무 건전성")
    col1, col2 = st.columns(2)
    with col1:
        filter_dict['D_E'] = st.checkbox("부채 비율 100% 미만")
    with col2:
        filter_dict['D_A'] = st.checkbox("자산 대비 부채 비율 50% 이하")

    st.subheader("부채 상환 능력")
    col1, col2 = st.columns(2)
    with col1:
        filter_dict['I_C'] = st.checkbox("이자 보상배율 2배 이상")
    with col2:
        filter_dict['D_EB'] = st.checkbox("부채/EBITDA 비율 3배 이하")

    st.subheader("성장 능력")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_dict['ROE'] = st.checkbox("ROE 증가")
    with col2:
        filter_dict['PBR'] = st.checkbox("PBR 증가")
    with col3:
        filter_dict['Net_income'] = st.checkbox("순이익 증가")
    with col4:
        filter_dict['Revenue'] = st.checkbox("매출 증가")

    st.subheader("주가")
    col1 = st.columns(1)[0]
    with col1:
        filter_dict['price_52'] = st.checkbox("52주 가격 중간값 이하")

   
    
    # 2행: 기간 선택
    st.subheader("필터링 기간 선택")
    period = st.radio("기간을 선택하세요:", ("2y", "5y", "10y", "max"), horizontal=True)
    st.write('주식 데이터와 기간이 맞지 않는 경우 자동으로 MAX로 지정합니다.')

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
                    
                    with st.container():  # 각 종목마다 컨테이너를 사용
                        x,y =(8,6)
                        st.subheader(f'{ticker} Financial Data')
                        col1, col2, col3, col4 = st.columns(4)  # 한 행에 4개의 열로 나누기
                        with col1:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.D_E_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('Debt_to_Equity_Ratio')
                        with col2:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.D_A_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('Debt_to_Asset_Ratio')
                        with col3:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.I_C_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('Interest_Coverage_Ratio')
                        with col4:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.D_EB_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('Debt_to_EBITDA_Ratio')

                        
                        col1, col2, col3, col4 = st.columns(4) 
                        with col1:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.PBR_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('PBR_graph')

                        with col2:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.ROE_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('ROE_graph')
                        
                        with col3:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.Revenue_Net_income_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('Revenue_Net_income_graph')
                        
                        with col4:
                            fig, ax = plt.subplots(figsize=(x,y))
                            stock.price_52_graph(True, ax=ax)  
                            st.pyplot(fig)  
                            st.write('price_52_graph')
    
                        
            except Exception as e:
                A=2
            #print(f'{ticker}검증 끝')
            
        
if __name__ == '__main__':
    main()


