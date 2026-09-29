import ActiveRidePanel from "../components/ride/ActiveRidePanel.jsx";
import PageLoader from "../components/common/PageLoader.jsx";
import SectionTitle from "../components/common/SectionTitle.jsx";
import RideHistory from "../components/history/RideHistory.jsx";
import { useActiveRide } from "../hooks/useActiveRide.js";

const RECENT_RIDES = 10;

export default function RidePage() {
  const { ride, loading, pending, message, endedCount, start, changeState, end } = useActiveRide();
  if (loading) return <PageLoader />;

  return (
    <>
      <ActiveRidePanel
        ride={ride}
        pending={pending}
        message={message}
        onStart={start}
        onChangeState={changeState}
        onEnd={end}
      />
      <SectionTitle>Historial de hoy</SectionTitle>
      <RideHistory limit={RECENT_RIDES} reloadKey={endedCount} />
    </>
  );
}
