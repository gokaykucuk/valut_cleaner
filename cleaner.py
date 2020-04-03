# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### Setup
# 

# %%
import re
import pandas as pd
import numpy as np
from tldextract import extract

dirty_passwords_file = "in.csv"
passwords_df = pd.read_csv(dirty_passwords_file)

# %% [markdown]
# ### Clean Uri's
# 

# %%
domain_extractor = re.compile(r'^(?:https?:)?(?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n]+)')

# print(passwords_df.login_uri)

def clean_login_uri(login_uri):
    if isinstance(login_uri, str):
        _, td, tsu = extract(login_uri)
        return td+'.'+tsu

passwords_df['login_uri'] = passwords_df['login_uri'].apply(clean_login_uri)

# %% [markdown]
# ### Find Duplicates

# %%
print("Before removing duplicates:")
print(passwords_df.count())
passwords_df.drop_duplicates(subset=['login_uri','login_username'], inplace=True, keep='last')

print("After removing duplicates:")
print(passwords_df.count())

# %% [markdown]
# ### Remove Specific Keywords

# %%
KEYWORDS = []

def isInKeywords(login_username):
    return any(map(lambda keyword: keyword in str(login_username),KEYWORDS))    

username_keywords_filter = passwords_df.login_username.apply(isInKeywords)

print(passwords_df.count())
passwords_df.mask(username_keywords_filter,inplace=True)
print(passwords_df.count())


# %% [markdown]
# ### Remove anything which is not login


# %% [markdown]
# ### Save the results

# %%
passwords_df.dropna(subset=['login_uri'], inplace=True)
passwords_df.to_csv('out.csv')



# %% [markdown]
### END