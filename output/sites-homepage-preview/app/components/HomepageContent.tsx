import Image from "next/image";
import { chapters, faqs, reviews, smsHref, smsVisitHref, states } from "../homepage-content";
import { ThreadPath } from "./ThreadPath";

const TextChris = ({ className }: { className?: string }) => (
  <a className={className} href={smsVisitHref}>
    Text Chris to start a $59 visit
  </a>
);

const headingText = (title: string) => title.replace(/\.$/, "");

export function HomepageContent() {
  return (
    <>
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <header className="site-header">
        <nav aria-label="Primary navigation">
          <a className="brand" href="#main-content" aria-label="NPCWoods home">NPCWoods</a>
          <a className="nav-cta" href={smsHref}>Text Chris</a>
        </nav>
      </header>

      <main id="main-content">
        <ThreadPath />

        <section className="chapter hero" aria-labelledby="chapter-1-title">
          <div className="chapter-copy">
            <p className="eyebrow">Chapter {chapters[0].number}</p>
            <h1 id="chapter-1-title">{headingText(chapters[0].title)}</h1>
            <p>{chapters[0].body}</p>
            <ul className="trust-list" aria-label="Visit details">
              <li>$59 flat fee</li>
              <li>Licensed in 11 states</li>
              <li>Usually back to you within an hour during business hours</li>
            </ul>
            <div className="hero-actions">
              <TextChris className="button button-primary" />
              <a className="button button-secondary" href="#friction">See how it works</a>
            </div>
          </div>
          <Image src="/chris-1000.webp" alt="Chris Woods, NP" width={768} height={768} priority sizes="(max-width: 720px) 100vw, 50vw" />
        </section>

        <section className="chapter" id="friction" aria-labelledby="chapter-2-title">
          <p className="eyebrow">Chapter {chapters[1].number}</p>
          <h2 id="chapter-2-title">{headingText(chapters[1].title)}</h2>
          <p>{chapters[1].body}</p>
          <ul className="obstacles" aria-label="Common obstacles">
            <li><span aria-hidden="true">01</span>Drive</li>
            <li><span aria-hidden="true">02</span>Wait</li>
            <li><span aria-hidden="true">03</span>Forms</li>
          </ul>
        </section>

        <section className="chapter guide" aria-labelledby="chapter-3-title">
          <Image src="/chris-400.webp" alt="Chris Woods, NP" width={400} height={400} sizes="(max-width: 720px) 70vw, 30vw" />
          <div className="chapter-copy">
            <p className="eyebrow">Chapter {chapters[2].number}</p>
            <h2 id="chapter-3-title">{headingText(chapters[2].title)}</h2>
            <p>{chapters[2].body}</p>
            <blockquote>“Just text me.”</blockquote>
            <span className="guide-thread-tail" aria-hidden="true" />
          </div>
        </section>

        <section className="chapter messages-chapter" aria-labelledby="chapter-4-title">
          <p className="eyebrow">Chapter {chapters[3].number}</p>
          <h2 id="chapter-4-title">{headingText(chapters[3].title)}</h2>
          <p>{chapters[3].body}</p>
          <ol className="message-list" aria-label="A typical text conversation">
            <li className="message visitor-message"><span>Visitor</span>“Here’s what’s going on…”</li>
            <li className="message chris-message"><span>Chris</span>“I’ve got it. Let me review this.”</li>
            <li className="message chris-message"><span>Chris</span>“Here are your next steps.”</li>
          </ol>
        </section>

        <section className="chapter resolution" aria-labelledby="chapter-5-title">
          <p className="eyebrow">Chapter {chapters[4].number}</p>
          <h2 id="chapter-5-title">{headingText(chapters[4].title)}</h2>
          <p>{chapters[4].body}</p>
          <div className="resolution-ring"><TextChris className="button button-primary" /></div>
        </section>

        <section className="reviews" aria-labelledby="reviews-title">
          <h2 id="reviews-title">Real texts. Real relief.</h2>
          <div className="review-grid">
            {reviews.map((review) => (
              <figure key={review.initials}>
                <blockquote>“{review.quote}”</blockquote>
                <figcaption>— {review.initials}</figcaption>
              </figure>
            ))}
          </div>
        </section>

        <section className="states" aria-labelledby="states-title">
          <h2 id="states-title">Licensed in 11 states.</h2>
          <ul>{states.map((state) => <li key={state}>{state}</li>)}</ul>
        </section>

        <section className="safety" aria-labelledby="safety-title">
          <h2 id="safety-title">Some symptoms need in-person care.</h2>
          <p>If symptoms are severe or life-threatening, call 911 or go to the nearest emergency department. Chris will plainly direct you to in-person or emergency care when appropriate.</p>
        </section>

        <section className="faq" aria-labelledby="faq-title">
          <h2 id="faq-title">Common questions</h2>
          {faqs.map((faq) => (
            <details key={faq.question}>
              <summary>{faq.question}</summary>
              <p>{faq.answer}</p>
            </details>
          ))}
        </section>

        <section className="final-cta" aria-labelledby="final-cta-title">
          <h2 id="final-cta-title">Feeling rough? Just text me.</h2>
          <TextChris className="button button-primary" />
        </section>
      </main>

      <aside className="mobile-text-bar" aria-label="Start a visit">
        <span>$59 flat fee</span>
        <TextChris className="button button-primary" />
      </aside>
    </>
  );
}
