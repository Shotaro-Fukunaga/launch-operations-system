import { FC, ReactNode } from 'react'
import { SideBar } from './SideBar'

type Props = {
  children: ReactNode
  isNavigateBlock?: boolean
  onConfirm?: () => void
}

export const BasicLayout: FC<Props> = ({ children }) => {
  return (
    <div className="flex flex-col w-screen h-screen overflow-hidden">
      {/* <Header setIsOpen={setIsOpen}></Header> */}
      <div className="relative flex h-full overflow-y-auto bg-gray-100 grow">
        <SideBar />
        <div className="h-full overflow-y-auto text-gray-700 grow">{children}</div>
      </div>
    </div>
  )
}
