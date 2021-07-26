import flask
from flask import request, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required
from flask_bcrypt import Bcrypt 
from flask_cors import CORS

import _strptime
import datetime
from datetime import timedelta
import dateutil
from dateutil.relativedelta import relativedelta, FR

import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
import numpy as np
import json
import os
import math
from ta import *
from werkzeug.security import safe_str_cmp
from functools import reduce

from bravisa_dash.dash_sector.sector import Sector
from bravisa_dash.dash_subsector.subsector import SubSector
from bravisa_dash.dash_industry.industry import Industry
from bravisa_dash.bravisa_perstock.perstock import Perstock

from bravisa_suite.suite import Suite

import helper
import bravisa_dash.helper as common


app = flask.Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# cloud_sql_proxy -instances=bravisa-temple-tree:asia-south1:btt-db=tcp:5444

import flask_login

import json
import time


with open('config.json','r') as f:
	config = json.load(f)

app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'BravisaTempleTreeEncryptedToken'


DBhost = config['DBLocal']['host']
DB = config['DBLocal']['DB']
DBuser = config['DBLocal']['DBuser']
DBPass = config['DBLocal']['DBPass']
DBPort = config['DBLocal']['DBPort']

def db_connect():
	if os.name == 'nt':
		conn = psycopg2.connect(database=DB, user=DBuser, password=DBPass, host=DBhost, port=DBPort)
		app.config["DEBUG"] = True
		return conn
	else:
		conn = psycopg2.connect(database="BravisaDB", user="sid", password="kayasid2018", host="/cloudsql/bravisa-temple-tree:asia-south1:btt-db", port="5432")
		return conn

def db_connect_local():
	conn = psycopg2.connect(database="newdb", user="postgres", password="postgres")
	app.config["DEBUG"] = True
	return conn


@app.route('/register', methods=['POST'])
def register():

	conn = helper.db_connect()
	cur = conn.cursor()
	
	username = request.json['username']
	password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')

	cur.execute("INSERT INTO \"public\".users (username, password) VALUES ('" +
		str(username) + "','" +
		str(password) + "')")

	conn.commit()
	result = {
		'username': username,
		'password': password
	}
	conn.close()

	return jsonify({'result': result})

@app.route('/login', methods=['POST'])
def login():

	conn = helper.db_connect()
	cur = conn.cursor()

	username = request.json['username']
	password = request.json['password']
	result = ""
	
	cur.execute("SELECT * FROM \"public\".users where username = '" + str(username) + "'")
	details = cur.fetchone()

	if bcrypt.check_password_hash(details[1], password):
		access_token = create_access_token(identity = {'username': details[0]}, expires_delta=timedelta(seconds=28800))
		result = jsonify({"token":access_token})
	else:
		result = jsonify({"error": "Invalid credentials"})
	
	conn.close()
	return result 

######################## End point for Suite ####################################
################################################################################

@app.route('/nhnl', methods=['GET']) 
@jwt_required
def nhnl_api():
    """
    NHNL table data for particular date
    """
    
    return Suite().nhnl_1yr()
	

@app.route('/prs', methods=['GET'])
@jwt_required
def prs_api():
    """
    PRS table data fetched for particular date
    """
    
    return Suite().prs()


@app.route('/maxdateprs', methods=['GET'])
@jwt_required
def maxdateprs_api():
    """
    fetched max date from PRS table
    """
    
    return Suite().maxdate_prs()


@app.route('/smr', methods=['GET'])
@jwt_required
def smr_api():
    """
    SMR table data fetched for particular date
    """
    
    return Suite().smr()


@app.route('/maxdatesmr', methods=['GET'])
@jwt_required
def maxdatesmr_api():
    """
    fetched Max date from SMR table
    """
    
    return Suite().maxdate_smr()


@app.route('/eps', methods=['GET'])
@jwt_required
def eps_api():
    """
    EPS table data fetched for particular date
    """
    
    return Suite().eps()

@app.route('/maxdateers', methods=['GET'])
@jwt_required
def maxdateers_api():
    """
    fetched Max date from EPS table
    """
    return Suite().maxdate_ers()

@app.route('/nse', methods=['GET'])
@jwt_required
def nse_api():
    """
    fetching the all data of NSE for particular date
    """
    
    return Suite().nse()


@app.route('/maxdatense', methods=['GET'])
@jwt_required
def maxdate_nse_api():
    """
    fetched Max date from NSE table
    """
    
    return Suite().maxdate_nse()


@app.route('/bse', methods=['GET'])
@jwt_required
def bse_api():
    """
    fetching the all data of BSE for particular date
    """
    
    return Suite().bse()


@app.route('/ext', methods=['GET', 'PUT'])
@jwt_required
def editExtValues_api():
    """
    Updates Extraordinary table based on user selection of include/exclude.
    Updates PAT, EPS, NPM, Q1 EPS Growth, 
    """
    
    return Suite().editExtValues()


@app.route('/frsmf', methods=['GET'])
@jwt_required
def frsmf_api():
    """
    fetching the all data of FRS-MFRank for particular date
    """
    
    return Suite().frs_mf_rank()
   

@app.route('/status', methods=['GET'])
@jwt_required
def status_api():
    """
    PRS report status
    """
    
    return Suite().prs_status() 

@app.route('/maxdatemf', methods=['GET'])
@jwt_required
def maxdatemf_api():
    """
    fetched Max date from FRS_MFRank  table
    """
    
    return Suite().maxdate_frs_mf()


@app.route('/frsnavcat', methods=['GET'])
@jwt_required
def frsnavcat_api():
    """
    fetch the all data from FRS-NAVCategoryAvg table for the particular date
    """
    
    return Suite().frs_navcat()


@app.route('/maxdatenavcat', methods=['GET'])
@jwt_required
def maxdatenavcat_api():
    """
    fetched Max date from FRS-NAVCategoryAvg  table
    """
    
    return Suite().maxdate_navrank()


@app.route('/frsnavrank', methods=['GET'])
@jwt_required
def frsnavrank_api():
    """
    fetch the all data from FRS-NAVRank  table for the particular date
    """
    
    return Suite().frs_navrank()


@app.route('/maxdatenavrank', methods=['GET'])
@jwt_required
def maxdatenavrank_api():
    """
    fetched Max date from FRS-NAVRank table
    """
    
    return Suite().maxdate_navrank()


@app.route('/indexhistory')
@jwt_required
def indexhistory_api():
    """
    fetch the all data from  IndexHistory table for the particular date
    """
    
    return Suite().indexhistory()


@app.route('/maxdatecombi', methods=['GET'])
@jwt_required
def maxdatecombi_api():
    
    """
    fetch the max date from the CombinedRS table
    """
    
    return Suite().maxdate_combi()


@app.route('/maxdateirs', methods=['GET'])
@jwt_required
def maxdateirs_api():
    """
    fetch the max date from the IRS table
    """
    
    return Suite().maxdate_irs()


@app.route('/irs')
@jwt_required
def irs_api():
    """
    fetch the all data from  IRS table for the particular date
    """
    
    return Suite().irs()


@app.route('/combirank', methods=['GET'])
@jwt_required
def combirank_api():
    """
    fetch the all data from  CombinedRS table for the particular date
    """
    
    return Suite().combirank()

@app.route('/mf_ohlc', methods=['GET'])
@jwt_required
def mf_ohlc_api():
    """
    fetching alll the MF_OHLC table data for the particular date
    """
    
    return Suite().mf_ohlc_data()



############################## endpoint for sector#########################

@app.route('/allstocksector', methods=['GET'])
@jwt_required
def allstocksector_api_api():
	""" Allstocks screen for particular Sector endpoint  """

	return Sector().allstock_sector()

@app.route('/sectordefault', methods=['GET'])
@jwt_required 
def sectordefault_api():
	""" Result for click on 'SECTOR' menu, All sector's IndexName, Close, PE, EPS, CompanyCount, Rank,Change 
            and  back day's performance """

	return Sector().sectordefault()

@app.route('/sec_performance', methods=['GET'])
@jwt_required
def sec_performance_api():
	""" For Performance tab, day back performance from the daily process 
		dash_process.index_performance' table  """

	return Sector().sec_performance()

@app.route('/sectoronselect', methods=['GET'])
@jwt_required
def sectoronselect_api():
	""" Returns all sector list for select box on individual sector """

	return Sector().sector_on_select()

@app.route('/indivi_sector', methods=['GET'])
@jwt_required
def indivi_sector_api():
	"""Returns data for individual Sector screen table 1 with basic details""" 

	return Sector().indivi_sector()

@app.route('/sectortop5', methods=['GET'])
@jwt_required
def sectortop5_api():
	""" Returns Top 5 RS stocks for Sector N screen   """
 
	return Sector().sector_top5_RS()

@app.route('/sectortop5earners', methods=['GET'])
@jwt_required
def sectortop5earners_api():
	"""Returns Top 5 Earning stocks for Sector N screen """

	return Sector().sector_top5_earners() 

@app.route('/sectortopcombi', methods=['GET'])
@jwt_required
def sectortopcombi_api():
	"""Returns Top 5 Combi RS stocks for Sector N screen"""

	return Sector().sector_topcombi()

@app.route('/rssector')
@jwt_required
def rssector_api():
	"""Returns Data for RS chart on Sector N screen"""

	return Sector().rssector()

@app.route('/sectoroffhighpercent', methods=['GET'])
@jwt_required
def sectoroffhighpercent_api():
	""" Returns data for OFF High chart based on a sector for 1 year on Sector N screen   """


	return Sector().sector_offhigh_percent()

@app.route('/sectordropdown', methods=['GET'])
@jwt_required
def sectordropdown_api():
	""" Returns data for sector selection dropdown on Sector N screen """

	return Sector().sector_dropdown()

@app.route('/nhnlsec')
@jwt_required
def nhnlsec_api():
	""" Returns data for NHNL chart for 1 year on Sector N screen """

	return Sector().nhnlsec()


@app.route('/dropdown_sector_industry')
@jwt_required
def dropdown_sector_df_api():
	""" Returns data for Industry that comes under sector """

	return Sector().dropdown_sector_click()


################################### endpoint for subsector######################

@app.route('/allstocksubsector', methods=['GET'])
@jwt_required
def allstocksubsector_api():
	"""Allstocks screen for particular subsector endpoint """

	return SubSector().allstock_subsector()

@app.route('/subsectoronselect', methods=['GET'])
@jwt_required
def subsectoronselect_api():
	""" Returns all subsector list for select box on individual sector """

	return SubSector().subsector_on_select()

@app.route('/subsectordefault', methods=['GET'])
@jwt_required
def subsectordefault_api():
	""" Result for click on 'SUBSECTOR' menu, All subsector's IndexName, Close, PE, EPS, CompanyCount, Rank,Change 
		and  back day's performance """
 
	return SubSector().subsector_default()

@app.route('/subsec_performance', methods=['GET'])
@jwt_required
def subsec_performance_api():
	""" For Performance tab, day back performance from the daily process """

	return SubSector().subsec_performance()

@app.route('/indivi_subsector', methods=['GET'])
@jwt_required
def indivi_subsector_api():
	"""Returns data for individual subsector screen table 1 with basic details"""

	return SubSector().indivi_subsector()	

@app.route('/subsectortop5', methods=['GET'])
@jwt_required
def subsectortop5_api():
	""" Returns Top 5 RS stocks for subsector N screen   """

	return SubSector().subsector_top5_RS()

@app.route('/subsectortop5earners', methods=['GET'])
@jwt_required
def subsectortop5earners_api():
	""" Returns Top 5 Earning stocks for subsector N screen  """

	return SubSector().subsector_top5_earners()

@app.route('/subsectortopcombi', methods=['GET'])
@jwt_required
def subsectortopcombi_api():
	"""Returns Top 5 Combi RS stocks for subsector N screen"""

	return SubSector().subsector_topcombi()

@app.route('/rssubsector')
@jwt_required
def rssubsector_api():
	"""Returns Data for RS chart on subsector N screen"""

	return SubSector().rssubsector()

@app.route('/subsectoroffhighpercent', methods=['GET'])
@jwt_required
def subsectoroffhighpercent_api():
	""" Returns data for OFF High chart based on a subsector for 1 year on subsector N screen """

	return SubSector().subsector_offhigh_percent()

@app.route('/subsectordropdown', methods=['GET'])
@jwt_required
def subsectordropdown_api():
	""" Returns data for subsector selection dropdown on subSector N screen  """

	return SubSector().subsector_dropdown()

@app.route('/nhnlsubsec')
@jwt_required
def nhnlsubsec_api():
	""" Returns data for NHNL chart for 1 year on subsector N screen """
	
	return SubSector().nhnlsubsec()




############################ endpoint for industry##############################

@app.route('/allstockindustry', methods=['GET'])
@jwt_required
def allstockindustry_api():
	""" Allstocks screen for particular industry endpoint  """
 
	return Industry().allstock_industry()

@app.route('/industry_to_index_screen', methods=['GET'])
@jwt_required
def industrydefault_api():
	""" Result for click on 'INDUSTRY' menu, All industry's IndexName, Close, PE, EPS, CompanyCount, Rank,Change 
		and  back day's performance  """

	return Industry().industry_subsector_performance()

@app.route('/indivi_industry', methods=['GET'])
@jwt_required
def indivi_industry_api():
	""" Fetch the industry name which is present in the 'IndustryMapping' table. """

	return Industry().indivi_industry()

@app.route('/industry_performance', methods=['GET'])
@jwt_required
def industry_performance():
	""" For Performance tab, day back performance from the daily process """

	return Industry().industry_performance()

@app.route('/industrytop5', methods=['GET'])
@jwt_required
def industrytop5_api():
	""" Returns Top 5 RS stocks for industry N screen  """

	return Industry().industry_top5_RS()

@app.route('/industrytop5earners', methods=['GET'])
@jwt_required
def industrytop5earners_api():
	""" Returns Top 5 Earning stocks for industryname N screen """

	return Industry().industry_top5_earners()

@app.route('/industrytopcombi', methods=['GET'])
@jwt_required
def industrytopcombi_api():
	""" Returns Top 5 Combi RS stocks for industryname N screen """

	return Industry().industry_topcombi()

@app.route('/rsindustry')
@jwt_required
def rsindustry_api():
	"""  Returns Data for RS chart on industryname N screen """

	return Industry().rsindustry()

@app.route('/industryoffhighpercent', methods=['GET'])
@jwt_required
def industryoffhighpercent_api():
	""" Returns data for OFF High chart based on a industryname for 1 year on industryname N screen  """

	return Industry().industry_offhigh_percent()

@app.route('/industryonselect', methods=['GET'])
@jwt_required
def industryonselect_api():
	""" Returns data for subsector selection dropdown on subSector N screen """

	return Industry().industry_on_select()

@app.route('/nhnlind')
@jwt_required
def nhnlind_api():
	""" Returns data for NHNL chart for 1 year on indname N screen  """

	return Industry().nhnlind()


@app.route('/industry_dropdown', methods=['GET'])
@jwt_required
def industry_dropdown():
    """ 
        Endpoint for Industry Dropdown on Industry Index page 
        Loads only IndustryIndexName
    """
    return Industry().industry_dropdown()

############################## Endpoint for Perstock #########################
##############################################################################

@app.route('/perstockgraphs')
@jwt_required
def perstockgraphs_api():
    """
    fetching one year of OHLC data for 
    Bravisa Dash graph
    """

    return Perstock().per_stock_graphs()


@app.route('/perstockprs')
@jwt_required
def perstockprs_api():
    """
    fetching one year of PRS data for
    Bravisa Dash graph
    """
    
    return Perstock().per_stock_prs()

@app.route('/perstockrrs')
@jwt_required
def perstockrrs_api():
    """
    fetching one year of SMR data for
    Bravisa Dash graph in front end this graph 
    name is ERS
    """
    
    return Perstock().per_stock_rrs()


@app.route('/perstockers')
@jwt_required
def perstockers_api():
    """
    fetching one year of EPS data for
    Bravisa Dash graph
    """
    
    return Perstock().per_stock_ers()

@app.route('/perstockfrs')
@jwt_required
def perstockfrs():
    """
    fetching one year of FRS-MFRank data for
    Bravisa Dash graph
    """
    
    return Perstock().per_stock_frs()

@app.route('/graphrangeohlc')
@jwt_required
def graphrange_api():
    """
    OHLC data fecthed from OHLC table for 
    Bravisa Dash Graph with range 1Week, 1month, 1Year
    """
    return Perstock().ohlc_graph_range()


@app.route('/price_sec', methods=['GET'])
@jwt_required
def price_sec():
    """Returns PE values for all sector from last year"""

    return common.price()

@app.route('/price_subsec', methods=['GET'])
@jwt_required
def price_subsec():
    """Returns PE values for all subsector from last year"""
    return common.price()

@app.route('/price_ind', methods=['GET'])
@jwt_required
def price_ind():
    """Returns PE values for all industry from last year"""
    return common.price()
	

@app.route('/offhighhomepage', methods=['GET'])
@jwt_required
def offhighhome_api():
    """
    Off-High percentage count data fetched from
    stock_off_high  table for the latest date
    """
    return Perstock().offhigh_count_percentage()


@app.route('/offlowhomepage', methods=['GET'])
@jwt_required
def offlowhomepage_api():
    """
    Off-Low percentage count data fetched from
    stock_off_high  table  fot the latest date
    """
    
    return Perstock().offlow_homepage()



@app.route('/topohlc')
@jwt_required 
def topohlc_api():
    """
    From IndexHistroy table fetching one year of
    OHLC data with parameter ticker name
    """
    
    return Perstock().top_ohlc()

@app.route('/graphrangeprs')
@jwt_required
def graphrangeprs_api():
    """
    Combined Strength, Date data fecthed from PRS table for 
    Bravisa Dash Graph with range 1Week, 1month, 1Year
    """
    
    return Perstock().graph_range_prs()


@app.route('/graphrangeirs')
@jwt_required
def graphrangeirs():
    """
    Rank, Date data fecthed from IRS table for 
    Bravisa Dash Graph with range 1Week, 1month, 1Year
    """
    
    return Perstock().graph_range_irs()

@app.route('/graphrangefrs')
@jwt_required
def graphrangefrs():
    """
    MFRank, Date data fecthed from FRS table for 
    Bravisa Dash Graph with range 1Week, 1month, 1Year
    """
    
    return Perstock().graph_range_frs()



@app.route('/graphrangerrs')
@jwt_required
def graphrangerrs_api():
    """
    SMR Rank, SMRDate data fecthed from SMR table for 
    Bravisa Dash Graph with range 1Week, 1month, 1Year
    """
    
    return Perstock().graph_range_rrs()

@app.route('/graphrangeers')
@jwt_required
def graphrangeers_api():
    """
    Ranking, EPSDate data fecthed from EPS table for 
    Bravisa Dash Graph with range 1Week, 1month, 1Year
    EPS is written as ers in fronted end
    """
    
    return Perstock().graph_range_ers()


@app.route('/graphrangeema')
@jwt_required
def graphrangeema_api():
    """
    ema (Exponential moving average) calculated according to the
    range for 1M, 1W, 1Y (1M = 1Month, 1W = 1Week, 1Y = 1year) 
    from the CLose column of OHLC table
    """
    
    return Perstock().graph_range_ema()

#######################function present in Perstock graphs over##########

########################Perstock  calculation function start#############
@app.route('/getallstocs') #need to change name of api
@jwt_required
def all_nsecode_searched():
    """
    Getting all NSECode with starting letter user going to type
    in front end 
    """
    
    return Perstock().get_nsecode_searched()

@app.route('/getstocks')  #need to change name of api
@jwt_required
def getallstocks_api():
    """
    get all data of BSECode, NSECode, CompanyName, CompanyCode
    columns from BTTList
    """
    
    return Perstock().bttlist_distinct()

@app.route('/stockcheck')
@jwt_required
def getstockchecks_api():
    """
    getting all the ohlc data with some specific columns
    such as NSECode, Company, CompanyCode and parameter by 
    term(NSECode)
    """
    
    return Perstock().get_all_ohlc()


@app.route('/fund_exp')
@jwt_required
def fund_exp_api():
    """
    Getting the changes values of the quantity for latest date
    to one month back from the MFMergeList table
    """
    
    return Perstock().fund_exposure_change()

@app.route('/peerstocks')
@jwt_required
def peerstocks():
    """
    Getting top5 CombiRS table data with latest date
    """
    
    return Perstock().top_combiRS()

@app.route('/ttmvalues')
@jwt_required
def ttmvalues_api():
    """
    limiting the PAT values into 2 decimals
    """
    
    return Perstock().ttm_pat_values()


@app.route('/top50combi', methods=['GET'])
@jwt_required
def top50_combirank_api():
    """
    Latest Top50 Rank from the CombinedRS table 
    """
    
    return Perstock().top50_combirank()

@app.route('/ttm', methods=['GET'])
@jwt_required
def ttm_api():
    """
    Last three year of EPS Growth Values from
    TTM table
    """
    
    return Perstock().ttm_3yr_eps_growth()


@app.route('/ttm20yr', methods=['GET'])
# @jwt_required
def ttm20yr_api():
    """
    Last 20 year ending of EPS Growth Values from
    TTM table
    """
    
    return Perstock().ttm_20yr_eps_growth()



@app.route('/quarterly_eps', methods=['GET'])
@jwt_required
def quarterly_eps_api():
    """
    Latest 5yr ending of Q1 EPS Growth,  EPS, PAT
    values from QuarterlyEPS table
    """
    
    return Perstock().quarterly_5yr_eps()


@app.route('/quarterly20yr_eps', methods=['GET'])
@jwt_required
def quarterly20yrPopup_eps_api():
    """
    Latest 20yr ending of all columns
    values from QuarterlyEPS table
    """
    
    return Perstock().quarterly_20yr_eps()

@app.route('/combiranks', methods=['GET'])
@jwt_required
def combiranks_api():
    """
    check stock in and out for last friday
    from CombinedRS table
    """
    
    return Perstock().stocks_in_out_lastfriday()


@app.route('/perstock', methods=['GET'])
@jwt_required
def perstock_api():
    """
    particular stock performance has been fetched from 
    stock_performance table
    """
    
    return Perstock().stock_performance()

@app.route('/perstocktab2', methods=['GET'])
@jwt_required
def perstocktab2_api():
    """
    The values showed in Bravisa Dash tab 2 had
    fetched from here  with particular company code
    """
    
    return Perstock().stock_reports()

@app.route('/perstocktab3', methods=['GET'])
@jwt_required
def perstocktab3():
    """
    The values showed in Bravisa Dash tab 3 had
    fetched from here with particular company code
    """
    
    return Perstock().stock_fundExposure()


@app.route('/perstocktab4', methods=['GET'])
@jwt_required
def perstocktab4_api():
    """
    The values showed in Bravisa Dash tab 4 had
    fetched from here with particular company code
    """
    
    return Perstock().stock_tab4_view()


@app.route('/perstockirs')
@jwt_required
def perstockirs_api():
    """
    one year of Rank and Gendate from
    IRS table based upon parameter company code
    """
    
    return Perstock().per_stock_irs()


@app.route('/ema', methods=['GET'])
@jwt_required
def ema_api():
    """
    1year of OHLC data fetched with the CLose values and
    EMA(Exponential Moving Everage) is calculated
    """
    
    return Perstock().ema()


if __name__=="__main__":
	app.debug = True
	app.run(host='127.0.0.1', port=8081)
