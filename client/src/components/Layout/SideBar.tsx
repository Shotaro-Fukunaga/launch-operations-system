import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import TimelineIcon from "@mui/icons-material/Timeline";
import PublicIcon from "@mui/icons-material/Public";
import { Link } from "react-router-dom";

export const SideBar = () => {
  const iconStyle = { color: "black", fontSize: "24px" };
  return (
    <>
      <div className="bg-gray-400 w-full h-full flex flex-col items-center justify-end py-[1rem] gap-2">
        <ul>
          <li>
            <Link to="/">
              <RocketLaunchIcon style={iconStyle} />
            </Link>
          </li>
          <li>
            <Link to="/">
              <TimelineIcon style={iconStyle} />
            </Link>
          </li>
          <li>
            <Link to="/">
              <PublicIcon style={iconStyle} />
            </Link>
          </li>
        </ul>
      </div>
    </>
  );
};
