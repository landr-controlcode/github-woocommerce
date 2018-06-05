from woocommerce import API
import requests, os

class Github:
    release = {}

    def getRelease(self, data):
        print(data)
        self.release = data
        topics = requests.get("https://api.github.com/repos/%s/topics"%self.release["repository"]["full_name"], headers={
            "authorization":"Bearer %s"%os.environ.get("github_token", None),
            "Accept":"application/vnd.github.mercy-preview+json"
        })
        tj = topics.json()
        self.release["categories"] = []
        for topic in tj['names']:
            self.release["categories"].append({
                'name':topic
            })
        readme = requests.get("https://api.github.com/repos/%s/contents/README.md?ref=v%s"%(self.release["repository"]["full_name"], self.release["release"]["tag_name"]), headers={
            'authorization':"Bearer %s"%os.environ.get("github_token", None),
            'Accept':'application/vnd.github.v3.raw'
        })
        self.release["readme"] = readme.text

class Bridge:
    categorie_ids = []

    def __init__(self):
        self.wcapi = API(
            url=os.environ.get("wc_endpoint", None),
            consumer_key=os.environ.get("wc_consumer_key", None),
            consumer_secret=os.environ.get("wc_consumer_secret", None),
            wp_api=True,
            verify_ssl=False,
            version="wc/v2",
            timeout=30
        )

    def category_tree_manage(self, cats, parent=0):
        category_id = parent
        for cat in cats:
            response = self.wcapi.get("products/categories?search=%s"%cat["name"])
            results = response.json()
            if len(results)>0:
                for result in results:
                    self.categorie_ids.append({"id":result["id"]})
                    category_id = result["id"]
            else:
                response = self.wcapi.post("products/categories", {
                    "name": cat["name"],
                    "parent": parent,
                    "image": {}
                })
                result = response.json()
                category_id = result["id"]
                self.categorie_ids.append({"id":category_id})
            if "children" in cat and len(cat["children"])>0:
                self.category_tree_manage(cat["children"], category_id)    
    
    def insert(self, data):
        github = Github()
        github.getRelease(data)
        self.category_tree_manage(github.release["categories"])
        response = self.wcapi.get("products?sku=%s-%s"%(github.release["repository"]["name"],github.release["repository"]["id"]))
        result = response.json()
        if(len(result)==0):
            response = self.wcapi.post("products",
                {
                    "name": github.release["repository"]["name"],
                    "type": "simple",
                    "regular_price": "0.0",
                    "virtual": True,
                    "downloadable": True,
                    "sku": "%s-%s"%(github.release["repository"]["name"],github.release["repository"]["id"]),
                    "sold_individually": True,
                    "description": github.release["readme"],
                    "short_description": github.release["repository"]["description"],
                    "categories": self.categorie_ids
                }
            )
            return response.json()
        else:
            response = self.wcapi.put("products/%s"%result[0]["id"],
                {
                    "name": github.release["repository"]["name"],
                    "description": github.release["readme"],
                    "short_description": github.release["repository"]["description"],
                    "categories": self.categorie_ids
                }
            )
            return response.json()

if __name__ == "__main__":
    pass
