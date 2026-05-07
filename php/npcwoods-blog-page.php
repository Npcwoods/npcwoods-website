<?php
/**
 * Plugin Name: NPCWoods Blog Archive Page
 * Description: Custom blog archive that matches the NPCWoods design system. Overrides the default WP block theme template.
 * Version: 1.0
 * Author: NPCWoods
 */

add_action('template_redirect', function() {
    // Match the blog archive page - check URL path directly as fallback
    $is_blog = is_home() || is_page('blog') || (trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/') === 'blog');
    if (!$is_blog) return;

    // Query published posts
    $posts = get_posts([
        'post_type'      => 'post',
        'post_status'    => 'publish',
        'posts_per_page' => 20,
        'orderby'        => 'date',
        'order'          => 'DESC',
    ]);

    $headshot = 'https://npcwoods.com/wp-content/uploads/2026/03/chris-woods-headshot.png';
    $logo = 'https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg';

    ?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog — Health Tips from a Nurse Practitioner | NPCWoods</title>
    <meta name="description" content="Health tips, patient education, and telehealth insights from Chris Woods, a double board-certified Nurse Practitioner. Practical advice you can actually use.">
    <link rel="canonical" href="https://npcwoods.com/blog/">
    <link rel="icon" href="<?php echo $logo; ?>">
    <link rel="apple-touch-icon" href="<?php echo $logo; ?>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <?php wp_head(); ?>
</head>
<body>
<?php
    // Include shared header
    $header_path = ABSPATH . 'shared/header-snippet.html';
    if (file_exists($header_path)) {
        echo file_get_contents($header_path);
    }
?>

<style>
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; -webkit-font-smoothing: antialiased; margin: 0; background: #F7F8FA; color: #2A2A2A; }

    /* Force nav to be solid white on blog page — not transparent like homepage */
    .npc-nav {
        position: sticky !important;
        background: rgba(255,255,255,0.97) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(229,231,235,0.7) !important;
    }
    .npc-nav.scrolled {
        box-shadow: 0 4px 24px rgba(0,0,0,0.06) !important;
    }

    .blog-hero-section {
        background: linear-gradient(160deg, #1a4fd4 0%, #2563EB 25%, #3b82f6 50%, #60a5fa 75%, #93c5fd 100%);
        padding: 80px 24px 100px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .blog-hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at 30% 50%, rgba(255,255,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .blog-hero-section h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        font-weight: 400;
        color: #FFFFFF;
        margin: 0 0 16px;
        position: relative;
        z-index: 1;
    }
    .blog-hero-section p {
        color: rgba(255,255,255,0.85);
        font-size: 1.1rem;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
        position: relative;
        z-index: 1;
    }
    .blog-hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 50px;
        padding: 6px 18px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
    }

    .blog-grid {
        max-width: 1000px;
        margin: -60px auto 60px;
        padding: 0 24px;
        position: relative;
        z-index: 2;
        display: grid;
        grid-template-columns: 1fr;
        gap: 24px;
    }

    .blog-card {
        background: #FFFFFF;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        border: 1px solid rgba(229,231,235,0.7);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-decoration: none;
        color: inherit;
        display: grid;
        grid-template-columns: 1fr;
    }

    .blog-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(37,99,235,0.12);
        border-color: rgba(37,99,235,0.2);
    }

    .blog-card.has-image {
        grid-template-columns: 340px 1fr;
    }

    .blog-card-image {
        width: 100%;
        height: 100%;
        min-height: 220px;
        object-fit: cover;
    }

    .blog-card-body {
        padding: 32px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .blog-card-date {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }

    .blog-card-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.35rem;
        font-weight: 400;
        color: #1A1A2E;
        line-height: 1.35;
        margin: 0 0 12px;
        letter-spacing: -0.3px;
    }

    .blog-card-excerpt {
        font-size: 0.92rem;
        color: #6B7280;
        line-height: 1.65;
        margin: 0 0 20px;
    }

    .blog-card-read {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #2563EB;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .blog-card-read svg {
        transition: transform 0.2s;
    }

    .blog-card:hover .blog-card-read svg {
        transform: translateX(4px);
    }

    .blog-card-author {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid #F3F4F6;
    }

    .blog-card-author img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }

    .blog-card-author span {
        font-size: 0.8rem;
        color: #9CA3AF;
        font-weight: 500;
    }

    .blog-empty {
        text-align: center;
        padding: 60px 24px;
        color: #9CA3AF;
        font-size: 1.1rem;
    }

    @media (max-width: 768px) {
        .blog-hero-section { padding: 100px 20px 60px; }
        .blog-hero-section h1 { font-size: 2rem; }
        .blog-card.has-image { grid-template-columns: 1fr; }
        .blog-card-image { min-height: 200px; max-height: 220px; }
        .blog-card-body { padding: 24px; }
        .blog-card-title { font-size: 1.15rem; }
        .blog-grid { margin-top: -30px; }
    }
</style>

<div class="blog-hero-section">
    <div class="blog-hero-badge">&#9825; From a Board-Certified NP</div>
    <h1>The Blog</h1>
    <p>Health tips, real talk, and practical advice from a double board-certified Nurse Practitioner. No jargon, no fluff — just stuff you can actually use.</p>
</div>

<div class="blog-grid">
<?php if (empty($posts)): ?>
    <div class="blog-empty">
        <p>No posts yet — check back soon!</p>
    </div>
<?php else: ?>
    <?php foreach ($posts as $post):
        $featured_id = get_post_thumbnail_id($post->ID);
        $featured_url = $featured_id ? wp_get_attachment_image_url($featured_id, 'large') : '';
        $excerpt = wp_trim_words(wp_strip_all_tags($post->post_content), 30, '...');
        $date = date('F j, Y', strtotime($post->post_date));
        $link = get_permalink($post->ID);
        $has_image = !empty($featured_url);
    ?>
    <a href="<?php echo esc_url($link); ?>" class="blog-card<?php echo $has_image ? ' has-image' : ''; ?>">
        <?php if ($has_image): ?>
        <img class="blog-card-image" src="<?php echo esc_url($featured_url); ?>" alt="<?php echo esc_attr($post->post_title); ?>">
        <?php endif; ?>
        <div class="blog-card-body">
            <div class="blog-card-date"><?php echo $date; ?></div>
            <h2 class="blog-card-title"><?php echo esc_html($post->post_title); ?></h2>
            <p class="blog-card-excerpt"><?php echo esc_html($excerpt); ?></p>
            <div class="blog-card-read">
                Read More
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </div>
            <div class="blog-card-author">
                <img src="<?php echo $headshot; ?>" alt="Chris Woods, NP">
                <span>Chris Woods, NP</span>
            </div>
        </div>
    </a>
    <?php endforeach; ?>
<?php endif; ?>
</div>

<?php
    // Include shared footer
    $footer_path = ABSPATH . 'shared/footer-snippet.html';
    if (file_exists($footer_path)) {
        echo file_get_contents($footer_path);
    }
    wp_footer();
?>
</body>
</html>
<?php
    exit;
});
