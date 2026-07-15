import { HomepageContent } from "./components/HomepageContent";
import { FollowThread } from "./components/FollowThread";

export default function Home() {
  return (
    <FollowThread>
      <HomepageContent />
    </FollowThread>
  );
}
