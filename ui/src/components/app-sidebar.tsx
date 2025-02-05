import {  Home,  Search, Settings, PersonStandingIcon } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

// Menu items.
const items = [
  {
    title: "Home",
    url: "/",
    icon: Home,
  },
  {
    title: "Search",
    url: "/",
    icon: Search,
  },
  {
    title: "Settings",
    url: "/settings",
    icon: Settings,
  },
  {
    title: "About Us",
    url: "/aboutus",
    icon: PersonStandingIcon,
  },
]

export function AppSidebar() {
  return (
    <Sidebar side="left" variant="floating">
      <SidebarHeader>
        <div className="text-center text-gray-500 text-2xl">
          Byte Locker
        </div>
      </SidebarHeader>
      <SidebarContent> 
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url} className="">
                      <item.icon className="text-md"/>
                      <span className="text-lg">{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <div className="text-center text-gray-400 text-sm">
          © 2025 Byte Locker. All rights reserved.
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}
