from functools import partial

from langchain_core.tools import tool, InjectedToolArg # a decorator
from langchain.agents import Tool
from langchain_community.utilities import (GoogleSearchAPIWrapper, GoogleSerperAPIWrapper,
                                           DuckDuckGoSearchAPIWrapper, SearchApiAPIWrapper)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing_extensions import Annotated


# api_key = "KJYsKyaNprThsCzRSp7Ai2HS"

def search_results(query, search_func):
    """Obtain search results."""

    results = search_func.results(query)
    return results
    # try:
    #     results = search_func.results(query, n_query)
    #     return results
    # except:
    #     return []

@tool
def get_search(query:str="", engine:str="ddg", k:int=40, api_key="KJYsKyaNprThsCzRSp7Ai2HS"): # get the top-k search results
    """Search for knowledge on the internet and return the results."""
    

    if engine == "google":
         search = GoogleSearchAPIWrapper(k=k)
    elif engine == "ddg":
         search = DuckDuckGoSearchAPIWrapper(max_results=k)
    elif engine == "sapi-google":
         search = SearchApiAPIWrapper(k=k, engine="google", searchapi_api_key=api_key)
    elif engine == "sapi-bing":
         search = SearchApiAPIWrapper(k=k, engine="bing", searchapi_api_key=api_key)
    elif engine == "sapi-ddg":
         search = SearchApiAPIWrapper(k=k, engine="duckduckgo", searchapi_api_key=api_key)
    
    search_res = partial(search_results, search_func=search, n_query=k)
    tool = Tool(
        name="Google Search Snippets",
        description="Search Google for recent results.",
        func=search_res,
    )
    ref_text = tool.run(query)
    
    if 'Result' not in ref_text.keys():
        return ref_text
    else:
        return None


# class DateUpdater(BaseModel):
#     date_start:str = Field(description="Most distant date.")
#     date_end:str = Field(description="Most recent date.")


class SearchTools:

     def __init__(self, date_start=None, date_end=None):

          self.date_start = date_start
          self.date_end = date_end

     def yield_search(self, name_suffix=None, update_docstring=True):
          
          # print(self.date_end)
          def get_search_dated(query:str, date_end:str=self.date_end,
                              date_start:str=self.date_start, engine:str="sapi-google", k:int=40, api_key="KJYsKyaNprThsCzRSp7Ai2HS"):
               """Search for the knowledge on the internet between date_start and date_end and return the results.
               If only date_end was specified, it means all information before date_end is included.

               Args:
                    date_start: most distant date for search.
                    date_end: most recent date for search.
               """
               
               api_key = "KJYsKyaNprThsCzRSp7Ai2HS"

               if engine == "google":
                    search = GoogleSearchAPIWrapper(k=k)
               elif engine == "ddg":
                    search = DuckDuckGoSearchAPIWrapper(max_results=k)
               elif engine == "sapi-google":
                    search = SearchApiAPIWrapper(k=k, engine="google", searchapi_api_key=api_key)
               elif engine == "sapi-bing":
                    search = SearchApiAPIWrapper(k=k, engine="bing", searchapi_api_key=api_key)
               elif engine == "sapi-ddg":
                    search = SearchApiAPIWrapper(k=k, engine="duckduckgo", searchapi_api_key=api_key)
               
               search_res = partial(search_results, search_func=search)
               tool = Tool(
                    name="Google Search Snippets",
                    description="Search Google for recent results.",
                    func=search_res,
               )
               try:
                    print('date_start is {}, date_end is {}'.format(self.date_start, self.date_end))
               except:
                    print('date_end is {}'.format(self.date_end))
               ref_text = tool.run(query, time_period_min=self.date_start, time_period_max=self.date_end)
               # print(ref_text)
               
               if 'Result' not in ref_text.keys():
                    return ref_text
               else:
                    return None

          if update_docstring:
               new_docstring = """Search for the knowledge on the internet between {} and {} and return the results.
               If only date_end was specified, it means all information before date_end is included.

               Args:
                    date_start: most distant date for search.
                    date_end: most recent date for search.
               """.format(self.date_start, self.date_end)

               get_search_dated.__doc__ = new_docstring
          
          if name_suffix is None:
               return get_search_dated
          else:
               get_search_dated.__name__ = 'get_search_within_' + name_suffix
               return get_search_dated

          # return get_search_dated

     def yield_multiple_search(self, starts, ends, suffixes):
          """Construct multiple search tools with different specification."""
          
          toolbox = []
          original_start = self.date_start
          original_end = self.date_end

          for start, end, suffix in zip(starts, ends, suffixes):
               self.date_start = start
               self.date_end = end
               toolbox.append(self.yield_search(name_suffix=suffix))

          self.date_start = original_start
          self.date_end = original_end

          return toolbox

# def get_search_dated(query:str="", engine:str="sapi-google", k:int=40, date_start:Annotated[str, InjectedToolArg]=None, date_end:Annotated[str, InjectedToolArg]='12/31/2003', api_key="KJYsKyaNprThsCzRSp7Ai2HS"):
# @tool(parse_docstring=True)
def get_search_dated(query:str, date_end:Annotated[str, InjectedToolArg]='12/31/2000', date_start:Annotated[str, InjectedToolArg]=None, engine:str="sapi-google", k:int=40, api_key="KJYsKyaNprThsCzRSp7Ai2HS"):
    """Search for the knowledge on the internet between date_start and date_end and return the results.
    If only date_end was specified, it means all information before date_end is included.

    Args:
        date_end: most recent date for search.
    """

    if engine == "google":
         search = GoogleSearchAPIWrapper(k=k)
    elif engine == "ddg":
         search = DuckDuckGoSearchAPIWrapper(max_results=k)
    elif engine == "sapi-google":
         search = SearchApiAPIWrapper(k=k, engine="google", searchapi_api_key=api_key)
    elif engine == "sapi-bing":
         search = SearchApiAPIWrapper(k=k, engine="bing", searchapi_api_key=api_key)
    elif engine == "sapi-ddg":
         search = SearchApiAPIWrapper(k=k, engine="duckduckgo", searchapi_api_key=api_key)
    
    search_res = partial(search_results, search_func=search)
    tool = Tool(
        name="Google Search Snippets",
        description="Search Google for recent results.",
        func=search_res,
    )
    try:
        print('date_start is {}, date_end is {}'.format(date_start, date_end))
    except:
        print('date_end is {}'.format(date_end))
    ref_text = tool.run(query, time_period_min=date_start, time_period_max=date_end)
    # print(ref_text)
    
    if 'Result' not in ref_text.keys():
        return ref_text
    else:
        return None


def get_search_dateset(query:str="", engine:str="sapi-google", k:int=100, date_start:str=None, date_end:str='12/31/2007', api_key="KJYsKyaNprThsCzRSp7Ai2HS"):
    """Search for the knowledge on the internet between date_start and date_end and return the results.
    If only date_end was specified, it means all information before date_end is included."""

    if engine == "google":
         search = GoogleSearchAPIWrapper(k=k)
    elif engine == "ddg":
         search = DuckDuckGoSearchAPIWrapper(max_results=k)
    elif engine == "sapi-google":
         search = SearchApiAPIWrapper(k=k, engine="google", searchapi_api_key=api_key)
    elif engine == "sapi-bing":
         search = SearchApiAPIWrapper(k=k, engine="bing", searchapi_api_key=api_key)
    elif engine == "sapi-ddg":
         search = SearchApiAPIWrapper(k=k, engine="duckduckgo", searchapi_api_key=api_key)
    
    search_res = partial(search_results, search_func=search, n_query=k)
    tool = Tool(
        name="Google Search Snippets",
        description="Search Google for recent results.",
        func=search_res,
    )
    ref_text = tool.run(query, time_period_min=date_start, time_period_max=date_end)
    
    if 'Result' not in ref_text.keys():
        return ref_text
    else:
        return None