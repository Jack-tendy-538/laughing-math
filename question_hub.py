# from lm import *
from .core import *

###### TACKLE YOUR ISSUE HERE######


Hub = [
    Question("从 n 个产品中有 m 个次品，现要选出 k 个次品,且每次抽取后不放回。问：选出 k 个次品有多少种情况？"
,default={'n':10,'m':3,'k':2},answer_template=lambda draft:f"""
        
解答问题：从 {draft.n} 个产品中有 {draft.m} 个次品，现要选出 {draft.k} 个次品，且每次抽取后放回（有放回抽样）。
问：选出 {draft.k} 个次品有多少种情况？

解：首先，由于{f"m==k，所以抽出m个次品与抽出{draft.equal('r','n-m')}个次品都符合要求"
if draft.m==draft.k else 
"m>k，所以必须抽出m个次品"}

抽出 {draft.k} 个次品的情况数为组合数 C({draft.m},{draft.k})，即：
{draft.equal('l','C(m,k)')}
{f"当m==k时，还要加上选出所有正品的情况，答案是{draft.l+C(r,n-m)}"
if draft.m==draft.k else
f"答案是{draft.l}"}
""")
]
###### END OF ISSUE######
