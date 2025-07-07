

export interface RedditPost {
  id: string;
  title: string;
  selftext: string;
  author: string;
  created: number;
  subreddit: string;
}

export const fetchRedditPosts = async (
  subreddit: string,
  limit = 10
): Promise<RedditPost[]> => {
  const url = `https://www.reddit.com/r/${subreddit}/new.json?limit=${limit}`;
  const response = await fetch(url);
  const data = await response.json();
  const posts: RedditPost[] = data.data.children.map((child: any) => ({
    id: child.data.id,
    title: child.data.title,
    selftext: child.data.selftext,
    author: child.data.author,
    created: child.data.created_utc,
    subreddit: child.data.subreddit,
  }));
  return posts;
};
