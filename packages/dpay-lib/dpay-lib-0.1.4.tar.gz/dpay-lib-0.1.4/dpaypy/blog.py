from dpaypy.account import Account
from dpaypy.post import Post
from dpaypy.instance import shared_dpay_instance
from dpaypy.utils import is_comment


class Blog(list):
    """ Obtain a list of blog posts of an account

        :param str account_name: Name of the account
        :param DPay dpay_instance: DPay() instance to use when accesing a RPC

    """
    def __init__(self, account_name, dpay_instance=None):
        self.dpay = dpay_instance or shared_dpay_instance()
        self.name = account_name
        self.refresh()

    def refresh(self):
        state = self.dpay.rpc.get_state("/@%s/blog" % self.name)
        posts = state["accounts"].get(self.name, {}).get("blog", [])
        r = []
        for p in posts:
            post = state["content"][p]
            r.append(Post(post, dpay_instance=self.dpay))
        super(Blog, self).__init__(r)

    def all(self):
        self.current_index = Account(self.name, dpay_instance=self.dpay).virtual_op_count()

        # prevent duplicates
        self.seen_items = set()

        while True:
            # fetch the next batch
            if self.current_index == 0:
                raise StopIteration

            limit = 1000
            if self.current_index < 1000:
                # avoid duplicates on last batch
                limit = 1000 - self.current_index
                self.current_index = 1000

            h = self.dpay.rpc.get_account_history(self.name, self.current_index, limit)
            if not h:
                raise StopIteration

            self.current_index -= 1000

            # filter out irrelevant items
            def blogpost_only(item):
                op_type, op = item[1]['op']
                return op_type == 'comment' and not is_comment(op)

            hist = filter(blogpost_only, h)
            hist = map(lambda x: x[1]['op'][1], hist)
            hist = [x for x in hist if x['author'] == self.name]

            # filter out items that have been already passed on
            # this is necessary because post edits create multiple entries in the chain
            hist_uniq = []
            for item in hist:
                if item['permlink'] not in self.seen_items:
                    self.seen_items.add(item['permlink'])
                    hist_uniq.append(item)

            for p in hist_uniq:
                yield Post(p, dpay_instance=self.dpay)
