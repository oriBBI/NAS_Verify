import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


class stock_invest():
    
    def __init__(self, ticker):
        try:
            self.stock = yf.Ticker(ticker)
            self.ticker  = ticker
            self.financials = self.stock.financials
            self.balance_sheet = self.stock.balance_sheet

        except Exception as e:
            raise ValueError(f'{self.ticker}는 오류로 제외합니다.')
            print(f'{self.ticker}는 오류로 제외합니다.', end=' ')
            
    def value_verify(self, value=False, loss=0.1, base=False, way=False):
        try:
            if base==False and way ==False:
                count =0
                for date in range(len(value)-1):
                    if (value.iloc[date] - value.iloc[date+1])>-(value.iloc[date+1]*loss):
                        count +=1
                if (len(value) - 1== count) & (value.iloc[-1] < value.iloc[0]):
                    return True
                else:
                    return False
            elif (base != False ) & (way!=False):
                if way == 'down':
                    result=(value <= base).all()
                    if result:
                        return True
                    else:
                        return False
                elif way =='up':
                    result=(value >= base).all()
                    if result:
                        return True
                    else:
                        return False
        except Exception as e:
            print(type(e), e)
            return False
    
    def draw_plot(self, value, name, baseline=False, ax=False):
        ax = plt.gca()
        plt.plot(value, label=f'{self.ticker} {name}')
        plt.title(f'{self.ticker} {name}')
        plt.xlabel('DATE')
        plt.ylabel(name)
        plt.grid(True)
        if baseline:
            plt.axhline(y=baseline, color='red', linestyle='-', linewidth=3)
        plt.legend([name, 'baseline'])

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
            try:
                # 연도별 첫 번째 날짜 가져오기
                matching_date = historical_data.index[historical_data.index.year == date.year][0]
    
            except:
                matching_date = historical_data.index[historical_data.index.year == date.year]
            
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
        
    def Net_income_verify(self,loss=0.1):
        self.Revenue_Net_income_graph()
        count = 0
        for date in range(len(self.net_income)-1):
            if (self.net_income.iloc[date] - self.net_income.iloc[date+1])>-(self.net_income.iloc[date+1]*loss):
                count +=1
        if (len(self.net_income) - 1== count) & (self.net_income.iloc[0] - self.net_income.iloc[-1] >self.net_income.iloc[-1]*0.3):
            return True
        else:
            return False


    
    def price_52_graph(self, show=False, ax=False):
        try:
            try:
                history = self.stock.history(period="1y")  # 1년(52주) 데이터 가져오기
            except Exception as e:
                history = self.stock.history(period='max')
            current_price = self.stock.history(period="1d")['Close'].iloc[-1]  # 현재 가격
            
            if show:
                ax = plt.gca()
                plt.boxplot(list(history['Close']))
                plt.title(f'{self.ticker} ROE')
                plt.ylabel('Price')
                # 현재 값 표시
                plt.scatter(x=1, y=current_price ,color="green", zorder=3, label=f"Current Value ({current_price:.2f})")
                plt.text(1, current_price+2, f"current_price\n{current_price:.2f}", color="green", ha="center")
               
        except Exception as e:
            return f"데이터를 가져오는 중 오류가 발생했습니다: {e}"
        


    def price_52_median_verify(self):
        try:
            try:
                history = self.stock.history(period="1y")  # 1년(52주) 데이터 가져오기
            except Exception as e:
                history = self.stock.history(period='max')
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
            return False
        
    #부채 비율 100% 미만 재무 구조 안정적
    def D_E_verify(self, loss=0.1):
        self.D_E_graph()
        result = self.value_verify(self.Debt_to_Equity_Ratio,base=100, way='down')
        return result

    def D_E_graph(self, show = False, ax=False):
        Debt = self.balance_sheet.loc['Total Debt']
        Equity = self.balance_sheet.loc['Stockholders Equity']
        self.Debt_to_Equity_Ratio = ((Debt / Equity) * 100).dropna()
        if show:

            self.draw_plot(self.Debt_to_Equity_Ratio, 'Debt_to_Equity_Ratio', 100)

    #자산 대비 부채 비율 50% 이하 안정적
    def D_A_verify(self, loss=0.1):
        self.D_A_graph()
        result = self.value_verify(self.Debt_to_Asset_Ratio,base=50, way='down')
        return result
    
    def D_A_graph(self, show=False, ax=False):
        Debt = self.balance_sheet.loc['Total Debt']
        assets = self.balance_sheet.loc['Total Assets']
        self.Debt_to_Asset_Ratio = ((Debt / assets)*100).dropna()
        if show:
            self.draw_plot(self.Debt_to_Asset_Ratio, 'Debt_to_Asset_Ratio',50)

    #이자 보상배율 2배 이상 안정적
    def I_C_verify(self, loss=0.1 ):
        self.I_C_graph()
        result = self.value_verify(self.Interest_Coverage_Ratio, base=2, way='up')
        return result

    def I_C_graph(self, show = False, ax=False):
        operating_income = self.financials.loc['Operating Income']
        Interest_Expense = self.financials.loc['Interest Expense']
        self.Interest_Coverage_Ratio = (operating_income / Interest_Expense).dropna()
        if show:
            self.draw_plot(self.Interest_Coverage_Ratio, 'Interest_Coverage_Ratio',2)

    #부채/EBITDA 비율 3배 이하 부채 상환능력 뛰어남남
    def D_EB_verify(self, loss =0.1):
        self.D_EB_graph()
        result = self.value_verify(self.Debt_to_EBITDA_Ratio, base=3, way='down')
        return result
    def D_EB_graph(self, show= False, ax=False):
        Debt = self.balance_sheet.loc['Total Debt']
        Ebitda = self.financials.loc['EBITDA']
        self.Debt_to_EBITDA_Ratio =(Debt/Ebitda).dropna()
        if show:
            self.draw_plot( self.Debt_to_EBITDA_Ratio, 'Debt_to_EBITDA_Ratio',3)


    def verify_stock(self, veri_dict=False, loss=0.1, period='max'):
        self.period = period
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
                    verify['price_52'] = self.price_52_median_verify()
                if veri_dict['D_A']:
                    verify['D_A'] = self.D_A_verify(loss)
                if veri_dict['I_C']:
                    verify['I_C'] = self.I_C_verify(loss)
                if veri_dict['D_EB']:
                    verify['D_EB'] = self.D_EB_verify(loss)
                if veri_dict['D_E']:
                    verify['D_E'] = self.D_E_verify(loss)

            if all(verify.values()):
                return verify
            else:
                return False
        except Exception as e:
            return False

