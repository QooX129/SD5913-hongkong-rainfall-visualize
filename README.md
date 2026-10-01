# Hong Kong Rainfall Visualizer
## The phenomenon
This visualizes the Hong Kong rainfall record as a graph. It provides two time frames: viewing the whole year and comparing it with other years, or looking at every single day in a month.  
It is useful for us to easily check the rainfall record, compare it between different years immediately, and predict the possibility of rain in the future. 

![rainfall_sample](out/rainfall_sample_1.png)

## The source
I fetch my data from the Hong Kong Observatory: [https://www.hko.gov.hk/tc/cis/dailyElement.htm?ele=RF&y=2026](https://www.hko.gov.hk/tc/cis/dailyElement.htm?ele=RF&y=2026)  
It provides various data, including but not limited to rainfall, temperature, and pressure.  
For easier program access, it can directly make a web request. 
```https://www.hko.gov.hk/cis/individual_day/daily_{year}.xml```  
Fill in the {year} with the target year to get the source data shown on this page. It will get every single element's data, every day, and follow with 12 data points, which represent 12 months in the whole year, and be stored as an XML file. In our case, only Rainfall(RF) is used and measured in (mm).

## What the picture shows
In my example, the image shown above displays several years together side by side and lowers the opacity of the compared years. You can easily observe the trends or characteristics of the rainfall over the years. For example, there is a significant rise in rainfall from May to September. 

## Run it
To generate single-year or single-month rainfall data. Use:
```
uv run plot.py
```
Enter a year and month when prompted. The generated image will be stored in `out/`.


To use the browser interface instead, run:

```
uv run --with streamlit --with matplotlib --with requests streamlit run streamlit_app.py
```
Then run [http://localhost:8501](http://localhost:8501)  
In whole-year mode, use **Compare with** to add up to four other years. Each
comparison year has an adjustable color and the shared opacity control. The primary year color is also adjustable.  
To display a single month, uncheck **Show the whole year** to switch to single-month mode.