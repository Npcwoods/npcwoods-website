<?php
/**
 * Plugin Name: NPCWoods WP Singular Plates
 * Description: Serves WordPress posts/pages that have no static HTML file. Does not call wp_head (singular canvas dies mid-head after the Aug 11 2026 PHP update).
 * Version: 1.0
 *
 * Static landing pages keep their own mu-plugin readfile() at priority 1.
 * This runs later and only plates leftovers.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function npcwoods_singular_plate_static_file( $path ) {
	$rel = trim( (string) $path, '/' );
	if ( $rel === '' ) {
		return '';
	}
	return ABSPATH . $rel . '/index.html';
}

function npcwoods_singular_plate_should_serve() {
	if ( is_admin() || is_feed() || is_front_page() || is_home() ) {
		return false;
	}
	if ( ! is_singular( array( 'post', 'page' ) ) ) {
		return false;
	}
	$path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
	$path = is_string( $path ) ? $path : '/';
	$skip = array( '/pay/', '/path-visit/', '/blog/' );
	foreach ( $skip as $prefix ) {
		if ( trailingslashit( $path ) === $prefix ) {
			return false;
		}
	}
	return true;
}

/**
 * If a static index.html exists for this path but no earlier mu-plugin
 * mapped it, serve the file here. Previously we returned false and fell
 * through to the block theme — that boot is what soft-hangs under
 * GoDaddy gateway rate limits (parallel /learn/* sweeps).
 */
function npcwoods_singular_plate_serve_static_if_present() {
	$path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
	$path = is_string( $path ) ? $path : '/';
	$file = npcwoods_singular_plate_static_file( $path );
	if ( ! $file || ! file_exists( $file ) ) {
		return false;
	}
	header( 'Content-Type: text/html; charset=UTF-8' );
	header( 'X-NPCWoods-Page: static-catch' );
	header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
	header( 'X-Content-Type-Options: nosniff' );
	header( 'X-Frame-Options: SAMEORIGIN' );
	header( 'Referrer-Policy: strict-origin-when-cross-origin' );
	header( 'Cache-Control: public, max-age=3600' );
	readfile( $file );
	exit;
}

function npcwoods_singular_plate_render() {
	if ( is_admin() || is_feed() || is_front_page() || is_home() ) {
		return;
	}
	if ( ! is_singular( array( 'post', 'page' ) ) ) {
		return;
	}
	$path = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
	$path = is_string( $path ) ? $path : '/';
	$skip = array( '/pay/', '/path-visit/', '/blog/' );
	foreach ( $skip as $prefix ) {
		if ( trailingslashit( $path ) === $prefix ) {
			return;
		}
	}

	// Catch-all for static HTML left unmapped by path-specific mu-plugins.
	npcwoods_singular_plate_serve_static_if_present();

	if ( ! npcwoods_singular_plate_should_serve() ) {
		return;
	}

	$post = get_queried_object();
	if ( ! ( $post instanceof WP_Post ) || $post->post_status !== 'publish' ) {
		return;
	}

	$title   = wp_strip_all_tags( get_the_title( $post ) );
	$excerpt = wp_strip_all_tags( get_the_excerpt( $post ) );
	if ( $excerpt === '' ) {
		$excerpt = 'Plain-language care notes from Chris Woods, NP. $59 text visit when it is a fit.';
	}
	$permalink = get_permalink( $post );
	$body      = apply_filters( 'the_content', $post->post_content );
	$sms       = 'sms:4806394722?body=' . rawurlencode( "Hi Chris, I'd like to start a $59 visit" );
	$logo      = 'https://npcwoods.com/wp-content/uploads/2026/03/npcwoods-logo.jpg';
	$headshot  = 'https://npcwoods.com/wp-content/uploads/2026/04/chris-woods-headshot-160.webp';

	header( 'Content-Type: text/html; charset=UTF-8' );
	header( 'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload' );
	header( 'X-Content-Type-Options: nosniff' );
	header( 'X-Frame-Options: SAMEORIGIN' );
	header( 'Referrer-Policy: strict-origin-when-cross-origin' );
	?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title><?php echo esc_html( $title ); ?> | NPCWoods</title>
	<meta name="description" content="<?php echo esc_attr( wp_html_excerpt( $excerpt, 155, '…' ) ); ?>">
	<link rel="canonical" href="<?php echo esc_url( $permalink ); ?>">
	<?php $npc_share = 'https://npcwoods.com/assets/img/share/pricing-1200x630.jpg'; $npc_share_alt = 'Chris Woods, NP, text visit card for NPCWoods. $59 flat.'; $npc_desc = wp_html_excerpt( $excerpt, 155, '…' ); ?>
	<?php if ( in_array( (int) $post->ID, array( 1006, 1007 ), true ) ) : ?><meta name="robots" content="noindex, follow"><?php endif; // /t/ and /t/click/ ad-log stubs (2026-10-17) ?>
	<meta property="og:type" content="article">
	<meta property="og:site_name" content="NPCWoods">
	<meta property="og:title" content="<?php echo esc_attr( $title ); ?>">
	<meta property="og:description" content="<?php echo esc_attr( $npc_desc ); ?>">
	<meta property="og:url" content="<?php echo esc_url( $permalink ); ?>">
	<meta property="og:image" content="<?php echo esc_url( $npc_share ); ?>">
	<meta property="og:image:width" content="1200">
	<meta property="og:image:height" content="630">
	<meta property="og:image:alt" content="<?php echo esc_attr( $npc_share_alt ); ?>">
	<meta name="twitter:card" content="summary_large_image">
	<meta name="twitter:title" content="<?php echo esc_attr( $title ); ?>">
	<meta name="twitter:description" content="<?php echo esc_attr( $npc_desc ); ?>">
	<meta name="twitter:image" content="<?php echo esc_url( $npc_share ); ?>">
	<meta name="twitter:image:alt" content="<?php echo esc_attr( $npc_share_alt ); ?>">
	<link rel="icon" href="<?php echo esc_url( $logo ); ?>">
	<link rel="stylesheet" href="/assets/css/site.css">
	<style>
		body { margin:0; background:#F7F8FA; color:#1A1A2E; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; }
		.npc-plate { max-width: 760px; margin: 0 auto; padding: 32px 20px 96px; }
		.npc-plate h1 { font-size: clamp(1.8rem, 4vw, 2.4rem); line-height: 1.2; margin: 24px 0 12px; }
		.npc-plate .npc-kicker { color:#2563EB; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
		.npc-plate .npc-body { font-size: 1.05rem; line-height: 1.7; color:#4A4A5A; }
		.npc-plate .npc-body img { max-width: 100%; height: auto; border-radius: 12px; }
		.npc-cta { display:inline-block; margin-top: 28px; background:#2563EB; color:#fff !important; -webkit-text-fill-color:#fff !important; text-decoration:none; font-weight:600; padding:14px 28px; border-radius:100px; }
		.npc-signoff { margin-top: 36px; color:#8E8E9A; font-size: 0.9rem; }
	</style>
</head>
<body>
<nav class="npc-nav" aria-label="Main navigation">
	<div class="npc-nav-inner">
		<a href="https://npcwoods.com/" class="npc-nav-logo">
			<img src="<?php echo esc_url( $headshot ); ?>" alt="NPCWoods" width="38" height="38">
			<div class="npc-nav-logo-text">
				<span class="npc-nav-logo-name">NPCWoods</span>
				<span class="npc-nav-logo-tag">Telemedicine</span>
			</div>
		</a>
		<a href="<?php echo esc_url( $sms ); ?>" class="npc-nav-cta">Text Chris · $59</a>
	</div>
</nav>
<main class="npc-plate">
	<p class="npc-kicker">Chris Woods, NP · $59 text visit</p>
	<h1><?php echo esc_html( $title ); ?></h1>
	<div class="npc-body">
		<?php echo $body; ?>
	</div>
	<p><a class="npc-cta" href="<?php echo esc_url( $sms ); ?>">Text (480) 639-4722</a></p>
	<p class="npc-signoff">Chris Woods, NP · MSN, APRN, FNP-C, AGACNP-BC · You only pay if he can treat you. This is not emergency care. Call 911 for emergencies.</p>
</main>
</body>
</html>
	<?php
	exit;
}

add_action( 'template_redirect', 'npcwoods_singular_plate_render', 5 );
