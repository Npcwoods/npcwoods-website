"use client";

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useEffect, useRef, type ReactNode } from "react";

gsap.registerPlugin(ScrollTrigger);

export function FollowThread({ children }: { children: ReactNode }) {
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;

    const select = gsap.utils.selector(root);
    const mm = gsap.matchMedia();
    const animated = select(
      ".thread-progress, .obstacles li, .guide > img, .guide-thread-tail, .message, .resolution-ring, .mobile-text-bar",
    );

    mm.add("(prefers-reduced-motion: reduce)", () => {
      root.dataset.motion = "reduced";
      gsap.set(animated, { clearProps: "all" });
      animated.forEach((element) => element.removeAttribute("style"));
    });

    mm.add("(prefers-reduced-motion: no-preference)", () => {
      root.dataset.motion = "full";
      const compact = window.matchMedia("(max-width: 760px)").matches;
      const main = select("main")[0];
      const thread = select(".thread-progress")[0];
      const friction = select("#friction")[0];
      const obstacles = select(".obstacles li");
      const guide = select(".guide")[0];
      const portrait = select(".guide > img")[0];
      const tail = select(".guide-thread-tail")[0];
      const messagesChapter = select(".messages-chapter")[0];
      const messages = select(".message");
      const resolution = select(".resolution")[0];
      const resolutionRing = select(".resolution-ring")[0];

      if (main && thread) {
        gsap.fromTo(
          thread,
          { strokeDasharray: 1, strokeDashoffset: 1 },
          {
            strokeDashoffset: 0,
            ease: "none",
            scrollTrigger: {
              trigger: main,
              start: "top top",
              endTrigger: resolution ?? main,
              end: resolution ? "center center" : "bottom bottom",
              scrub: compact ? 0.25 : 0.5,
            },
          },
        );
      }

      if (friction && obstacles.length) {
        gsap.to(obstacles, {
          x: (index) => (index - 1) * (compact ? 12 : 24),
          opacity: 0.68,
          ease: "none",
          stagger: 0.04,
          scrollTrigger: {
            trigger: friction,
            start: "top 58%",
            end: "bottom 28%",
            scrub: true,
          },
        });
      }

      if (guide && portrait) {
        gsap.from(portrait, {
          x: compact ? -18 : -42,
          y: compact ? 12 : 24,
          scale: compact ? 0.98 : 0.94,
          opacity: 0.58,
          ease: "power2.out",
          scrollTrigger: {
            trigger: guide,
            start: "top 78%",
            end: "center 48%",
            scrub: compact ? 0.35 : 0.7,
          },
        });
      }

      if (guide && tail) {
        gsap.fromTo(
          tail,
          { scaleX: 0 },
          {
            scaleX: 1,
            ease: "none",
            scrollTrigger: {
              trigger: guide,
              start: "center 62%",
              end: "bottom 38%",
              scrub: true,
            },
          },
        );
      }

      if (messagesChapter && messages.length) {
        gsap.from(messages, {
          y: compact ? 14 : 24,
          scale: compact ? 0.99 : 0.97,
          opacity: 0.18,
          stagger: 0.3,
          ease: "none",
          scrollTrigger: {
            trigger: messagesChapter,
            start: "top 52%",
            end: "bottom 48%",
            scrub: compact ? 0.25 : 0.5,
          },
        });
      }

      if (resolution && resolutionRing) {
        gsap.from(resolutionRing, {
          scale: compact ? 0.92 : 0.84,
          opacity: 0.52,
          ease: "power2.out",
          scrollTrigger: {
            trigger: resolution,
            start: "top 70%",
            end: "center 48%",
            scrub: compact ? 0.3 : 0.6,
          },
        });
      }
    });

    return () => mm.revert();
  }, []);

  return (
    <div className="follow-thread-root" ref={rootRef}>
      {children}
    </div>
  );
}
