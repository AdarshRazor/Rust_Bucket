type BlogPostCardProps = {
    post: any;
  };
  
  export default function BlogPostCard({ post }: BlogPostCardProps) {
    const props = post.properties;
    const title = props.Title.title[0]?.plain_text || 'No Title';
    const status = props.Status.select?.name || 'No Status';
    const tags = props.Tags.multi_select || [];
    const content = props.Content.rich_text[0]?.plain_text || '';
    const date = props.Date.date?.start || '';
    const headerImage = props["Header Image"].files[0]?.file?.url || null;
  
    return (
      <div className="border rounded-lg p-4 mb-4 w-full max-w-xl bg-white shadow">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs px-2 py-1 rounded bg-green-600">{status}</span>
          <span className="text-xs text-gray-500">{date}</span>
        </div>
        <h2 className="text-xl font-bold mb-2 text-black">{title}</h2>
        {headerImage && (
          <img src={headerImage} alt={title} className="w-full h-40 object-cover rounded mb-2" />
        )}
        <div className="flex flex-wrap gap-2 mb-2">
          {tags.map((tag: any) => (
            <span
              key={tag.id}
              className={`text-xs px-2 py-1 rounded bg-red-600`}
              style={{ background: `var(--${tag.color})` }}
            >
              {tag.name}
            </span>
          ))}
        </div>
        <p className="text-gray-700">{content}</p>
      </div>
    );
  }