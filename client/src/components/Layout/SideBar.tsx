import RocketLaunchIcon from '@mui/icons-material/RocketLaunch'
import TimelineIcon from '@mui/icons-material/Timeline'
import PublicIcon from '@mui/icons-material/Public'
import { Link } from 'react-router-dom'

export const SideBar = () => {
  return (
    <>
      <div className="bg-gray-400 w-[4rem] h-full flex flex-col p-3">
        <ul>
          <li>
            <Link to="/">
              <RocketLaunchIcon style={{ color: 'black', fontSize: '24px' }} />
            </Link>
          </li>
          <li>
            <Link to="/">
              <TimelineIcon style={{ color: 'black', fontSize: '24px' }} />
            </Link>
          </li>
          <li>
            <Link to="/">
              <PublicIcon style={{ color: 'black', fontSize: '24px' }} />
            </Link>
          </li>
        </ul>
      </div>
    </>
  )
}
