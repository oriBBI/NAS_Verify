import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

class stock_invest():
    
    def __init__(self, ticker):
        try:
            self.stock = yf.Ticker(ticker)
            self.ticker  = ticker
            

        except Exception as e:
            raise ValueError(f'{self.ticker}는 오류로 제외합니다.')
            print(f'{self.ticker}는 오류로 제외합니다.', end=' ')
            

    
    def PBR_graph(self, show = False, ax= False):
        # 재무 데이터 가져오기
        financials = self.stock.financials
        balance_sheet = self.stock.balance_sheet
        try:
            historical_data = self.stock.history(period=self.period)
            historical_data.index = historical_data.index.tz_localize(None)
        except Exception as e:
            if type(e) == AttributeError:
                historical_data = self.stock.history(period='max')
                historical_data.index = historical_data.index.tz_localize(None)
        
        shareholder_equity = balance_sheet.loc['Stockholders Equity']
       
        pbr=[]
        for date in shareholder_equity.index:
            # 연도별 첫 번째 날짜 가져오기
            matching_date = historical_data.index[historical_data.index.year == date.year][0]
            
            # PBR 계산
            pbr_value = historical_data['Close'][matching_date] / (shareholder_equity[date])
            pbr.append(pbr_value)
        # PBR 시계열로 저장
        self.pbr_series = pd.Series(pbr, index=shareholder_equity.index).dropna()

        if show:
            # PBR 그래프 그리기
            ax = plt.gca()
            plt.plot(self.pbr_series, label=f'{self.ticker} PBR')
            plt.title(f'{self.ticker} PBR')
            plt.xlabel('DATE')
            plt.ylabel('PBR')
            plt.legend()
            plt.grid(True)

    def PBR_verify(self,loss):
        count = 0
        self.PBR_graph()
        for date in range(len(self.pbr_series)-1):
            if (self.pbr_series.iloc[date] - self.pbr_series.iloc[date+1])>-(self.pbr_series.iloc[date+1]*loss):
                count +=1
        if (len(self.pbr_series) - 1== count) & (self.pbr_series.iloc[-1] < self.pbr_series.iloc[0]):
            return True
        else:
            return False

    def ROE_graph(self, show = False, ax= False):
        financials = self.stock.financials
        balance_sheet = self.stock.balance_sheet
        try:
            historical_data = self.stock.history(period=self.period)
            historical_data.index = historical_data.index.tz_localize(None)
        except Exception as e:
            if type(e) == AttributeError:
                historical_data = self.stock.history(period='max')
                historical_data.index = historical_data.index.tz_localize(None)
        net_income = financials.loc['Net Income']
        shareholder_equity = balance_sheet.loc['Stockholders Equity']


        roe=[]
        for date in net_income.index:
            roe.append(net_income[date] / shareholder_equity[date])
        self.roe_series = pd.Series(roe, index = net_income.index).dropna()

        if show:
            # ROE 그래프 그리기
            ax = plt.gca()
            plt.plot(self.roe_series, label=f'{self.ticker} ROE')
            plt.title(f'{self.ticker} ROE')
            plt.xlabel('DATE')
            plt.ylabel('ROE')
            plt.legend()
            plt.grid(True)

    def ROE_verify(self,loss):
        self.ROE_graph()
        count = 0
        for date in range(len(self.roe_series)-1):
            if (self.roe_series.iloc[date] - self.roe_series.iloc[date+1])>-(self.roe_series.iloc[date+1]*loss):
                count +=1
        if (len(self.roe_series) - 1== count) & (self.roe_series.iloc[-1] < self.roe_series.iloc[0]):
            return True
        else:
            return False


    def Revenue_Net_income_graph(self, show = False, ax= False):
        income_statement = self.stock.income_stmt
        self.revenue = income_statement.loc['Total Revenue'].dropna()
        self.net_income = income_statement.loc['Net Income'].dropna()

        if show:
            ax = plt.gca()
            plt.plot(self.revenue, label=f'{self.ticker} revenue')
            plt.plot(self.net_income, label=f'{self.ticker} net_income')
            plt.title(f'{self.ticker} Revenue, net_income')
            plt.xlabel('DATE')
            plt.ylabel('revenue, net_income')
            plt.legend()
            plt.grid(True)
           
    def Revenue_verify(self,loss):
        self.Revenue_Net_income_graph()
        count = 0
        for date in range(len(self.revenue)-1):
            if (self.revenue.iloc[date] - self.revenue.iloc[date+1])>-(self.revenue.iloc[date+1]*loss):
                count +=1
        if (len(self.revenue) - 1== count) & (self.revenue.iloc[-1] < self.revenue.iloc[0]):
            return True
        else:
            return False
        
    def Net_income_verify(self,loss):
        self.Revenue_Net_income_graph()
        count = 0
        for date in range(len(self.net_income)-1):
            if (self.net_income.iloc[date] - self.net_income.iloc[date+1])>-(self.net_income.iloc[date+1]*loss):
                count +=1
        if (len(self.net_income) - 1== count) & (self.net_income.iloc[-1] < self.net_income.iloc[0]):
            return True
        else:
            return False


    
    def price_52_graph(self, show=False, ax=False):
        try:
            try:
                history = self.stock.history(period="1y")  # 1년(52주) 데이터 가져오기
            except Exception as e:
                if type(e) == AttributeError:
                    history = self.stock.history(period="max")
            high_52w = history['High'].max()  # 52주 고가
            low_52w = history['Low'].min()    # 52주 저가
            current_price = self.stock.history(period="1d")['Close'].iloc[-1]  # 현재 가격
            
            if show:
                ax = plt.gca()
                plt.boxplot(list(history['Close']))
                plt.title(f'{self.ticker} ROE')
                plt.ylabel('Price')
                # 현재 값 표시
                plt.scatter(x=1, y=current_price ,color="green", zorder=3, label=f"Current Value ({current_price:.2f})")
                plt.text(1, current_price+2, f"current_price\n{current_price:.2f}", color="green", ha="center")
                
                plt.show()
            
        except Exception as e:
            return f"데이터를 가져오는 중 오류가 발생했습니다: {e}"
        


    def price_52_median_veirify(self):
        try:
            try:
                history = self.stock.history(period="1y")  # 1년(52주) 데이터 가져오기
            except Exception as e:
                if type(e) == AttributeError:
                    history = self.stock.history(period="max")
            high_52w = history['High'].max()  # 52주 고가
            low_52w = history['Low'].min()    # 52주 저가
            current_price = self.stock.history(period="1d")['Close'].iloc[-1]  # 현재 가격
            
            # 52주 중간값 계산
            median_52w = (high_52w + low_52w) / 2

            # 현재 가격과 52주 중간값 비교
            if current_price < median_52w:
                return True
            else:
                return False
        except Exception as e:
            return f"데이터를 가져오는 중 오류가 발생했습니다: {e}"
        

    def verify_stock(self, veri_dict=False, loss=0.1, period='max'):
        self.period = "10y"
        try:
            verify = {}
            if veri_dict:
                if veri_dict['ROE']:
                    verify['ROE'] = self.ROE_verify(loss)
                if veri_dict['PBR']:
                    verify['PBR'] = self.PBR_verify(loss)
                if veri_dict['Revenue']:
                    verify['Revenue'] = self.Revenue_verify(loss)
                if veri_dict['Net_income']:
                    verify['Net_income'] = self.Net_income_verify(loss)
                if veri_dict['price_52']:
                    verify['price_52'] = self.price_52_median_veirify()

            
            if all(verify.values()):
                print(self.ticker, verify)
                return verify
            else:
                return False
        except Exception as e:
            print(f'{self.ticker}는 {e}오류로 제외합니다.', end=' ')
            return False



