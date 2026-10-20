import { useEffect, useState } from 'react'
import { addPostComment, createPost, getPosts, togglePostLike } from '../../api/socialAPI'
import LoadingSpinner from '../common/LoadingSpinner'

export default function SocialFeed() {
  const [posts, setPosts] = useState([])
  const [draft, setDraft] = useState('')
  const [commentDrafts, setCommentDrafts] = useState({})
  const [loading, setLoading] = useState(true)
  const [posting, setPosting] = useState(false)

  const loadPosts = () => getPosts().then(({ data }) => setPosts(data)).catch(() => {}).finally(() => setLoading(false))
  useEffect(() => { loadPosts() }, [])

  const publish = async (event) => {
    event.preventDefault()
    if (!draft.trim()) return
    setPosting(true)
    try {
      const { data } = await createPost(draft.trim())
      setPosts((current) => [data, ...current])
      setDraft('')
    } finally { setPosting(false) }
  }

  const like = async (postId) => {
    const { data } = await togglePostLike(postId)
    setPosts((current) => current.map((post) => post.id === postId ? { ...post, liked_by_me: data.liked_by_me, likes_count: data.likes_count } : post))
  }

  const comment = async (event, postId) => {
    event.preventDefault()
    const body = commentDrafts[postId]?.trim()
    if (!body) return
    const { data } = await addPostComment(postId, body)
    setPosts((current) => current.map((post) => post.id === postId ? { ...post, comments: [...post.comments, data] } : post))
    setCommentDrafts((current) => ({ ...current, [postId]: '' }))
  }

  if (loading) return <LoadingSpinner />

  return <section style={{ display: 'grid', gap: '0.8rem' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', gap: '1rem' }}><div><p style={{ color: '#a78bfa', fontSize: '0.72rem', letterSpacing: '0.14em', fontWeight: 800, margin: 0 }}>THE CAPABILITY FEED</p><h2 style={{ margin: '0.3rem 0 0' }}>What is moving the field</h2></div><span style={{ color: '#94a3b8', fontSize: '0.78rem' }}>Live network notes</span></div>
    <form onSubmit={publish} style={{ display: 'flex', gap: '0.6rem', alignItems: 'center', padding: '0.7rem', background: 'rgba(15,23,42,0.82)', border: '1px solid rgba(148,163,184,0.14)', borderRadius: '0.9rem' }}><input value={draft} onChange={(event) => setDraft(event.target.value)} placeholder="Share a useful win, question, or insight..." aria-label="Create a post" style={{ flex: 1 }} /><button disabled={posting} className="btn-primary">{posting ? 'Posting...' : 'Post'}</button></form>
    {posts.map((post) => <article key={post.id} style={{ padding: '1rem', background: 'rgba(15,23,42,0.82)', border: '1px solid rgba(148,163,184,0.14)', borderRadius: '0.9rem' }}><div style={{ display: 'flex', gap: '0.7rem', alignItems: 'center' }}><div style={{ width: '40px', height: '40px', borderRadius: '50%', display: 'grid', placeItems: 'center', background: '#8b5cf6', color: '#fff', fontWeight: 900 }}>{post.author_name.slice(0, 2).toUpperCase()}</div><div><strong>{post.author_name}</strong><div style={{ color: '#94a3b8', fontSize: '0.75rem' }}>{post.author_role} · {post.topic}</div></div></div><p style={{ color: '#e2e8f0', lineHeight: 1.7, margin: '0.9rem 0' }}>{post.body}</p>{post.source_url && <a href={post.source_url} target="_blank" rel="noreferrer" style={{ color: '#7dd3fc', fontSize: '0.78rem' }}>Read source: {post.source_name}</a>}<div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.9rem' }}><button onClick={() => like(post.id)} style={{ background: post.liked_by_me ? 'rgba(244,63,94,0.18)' : 'rgba(148,163,184,0.1)', color: post.liked_by_me ? '#fb7185' : '#cbd5e1' }}>{post.liked_by_me ? '♥' : '♡'} {post.likes_count}</button><span style={{ padding: '0.4rem 0.65rem', color: '#94a3b8', fontSize: '0.8rem' }}>{post.comments.length} comments</span></div><form onSubmit={(event) => comment(event, post.id)} style={{ display: 'flex', gap: '0.5rem', marginTop: '0.7rem' }}><input value={commentDrafts[post.id] || ''} onChange={(event) => setCommentDrafts((current) => ({ ...current, [post.id]: event.target.value }))} placeholder="Add a thoughtful comment..." aria-label={`Comment on ${post.author_name}'s post`} /><button className="btn-outline">Reply</button></form>{post.comments.length > 0 && <div style={{ display: 'grid', gap: '0.35rem', marginTop: '0.7rem', paddingLeft: '1rem', borderLeft: '2px solid rgba(148,163,184,0.18)' }}>{post.comments.slice(-3).map((comment) => <div key={`${comment.author_name}-${comment.created_at}`} style={{ color: '#cbd5e1', fontSize: '0.8rem' }}><strong>{comment.author_name}</strong> {comment.body}</div>)}</div>}</article>)}
  </section>
}
