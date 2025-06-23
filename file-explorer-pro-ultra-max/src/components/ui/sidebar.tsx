"use client"

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { VariantProps, cva } from "class-variance-authority"
import { PanelLeft } from "lucide-react"

import { useIsMobile } from "@/hooks/use-mobile"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Sheet, SheetContent } from "@/components/ui/sheet"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

const SIDEBAR_COOKIE_NAME = "sidebar_state"
const SIDEBAR_WIDTH_COOKIE_NAME = "sidebar_width"
const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 7
const SIDEBAR_WIDTH = 256 // default width in pixels
const SIDEBAR_WIDTH_MOBILE = "18rem"
const SIDEBAR_WIDTH_ICON = "3rem"
const SIDEBAR_KEYBOARD_SHORTCUT = "b"

type SidebarContext = {
  state: "expanded" | "collapsed"
  open: boolean
  setOpen: (open: boolean) => void
  openMobile: boolean
  setOpenMobile: (open: boolean) => void
  isMobile: boolean
  toggleSidebar: () => void
  width: number
  isResizing: boolean
  handleMouseDown: (e: React.MouseEvent) => void
}

const SidebarContext = React.createContext<SidebarContext | null>(null)

function useSidebar() {
  const context = React.useContext(SidebarContext)
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider.")
  }

  return context
}

const SidebarProvider = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> & {
    defaultOpen?: boolean
    open?: boolean
    onOpenChange?: (open: boolean) => void
  }
>(
  (
    {
      defaultOpen = true,
      open: openProp,
      onOpenChange: setOpenProp,
      className,
      style,
      children,
      ...props
    },
    ref
  ) => {
    const isMobile = useIsMobile()
    const [openMobile, setOpenMobile] = React.useState(false)
    const [width, setWidth] = React.useState(SIDEBAR_WIDTH)
    const [isResizing, setIsResizing] = React.useState(false)

    React.useEffect(() => {
      const savedWidth = localStorage.getItem(SIDEBAR_WIDTH_COOKIE_NAME)
      if (savedWidth) {
        setWidth(JSON.parse(savedWidth))
      }
    }, [])

    const handleMouseDown = (e: React.MouseEvent) => {
      e.preventDefault()
      e.stopPropagation()
      setIsResizing(true)
      document.body.style.cursor = "col-resize"
    }

    const handleMouseUp = React.useCallback(() => {
      if (isResizing) {
        setIsResizing(false)
        document.body.style.cursor = "auto"
        localStorage.setItem(SIDEBAR_WIDTH_COOKIE_NAME, JSON.stringify(width))
      }
    }, [isResizing, width])

    const handleMouseMove = React.useCallback(
      (e: MouseEvent) => {
        if (isResizing) {
          const newWidth = e.clientX
          if (newWidth > 200 && newWidth < 500) {
            setWidth(newWidth)
          }
        }
      },
      [isResizing]
    )

    React.useEffect(() => {
      window.addEventListener("mousemove", handleMouseMove)
      window.addEventListener("mouseup", handleMouseUp)

      return () => {
        window.removeEventListener("mousemove", handleMouseMove)
        window.removeEventListener("mouseup", handleMouseUp)
      }
    }, [handleMouseMove, handleMouseUp])

    const [_open, _setOpen] = React.useState(defaultOpen)
    const open = openProp ?? _open
    const setOpen = React.useCallback(
      (value: boolean | ((value: boolean) => boolean)) => {
        const openState = typeof value === "function" ? value(open) : value
        if (setOpenProp) {
          setOpenProp(openState)
        } else {
          _setOpen(openState)
        }

        document.cookie = `${SIDEBAR_COOKIE_NAME}=${openState}; path=/; max-age=${SIDEBAR_COOKIE_MAX_AGE}`
      },
      [setOpenProp, open]
    )

    const toggleSidebar = React.useCallback(() => {
      return isMobile
        ? setOpenMobile((open) => !open)
        : setOpen((open) => !open)
    }, [isMobile, setOpen, setOpenMobile])

    React.useEffect(() => {
      const handleKeyDown = (event: KeyboardEvent) => {
        if (
          event.key === SIDEBAR_KEYBOARD_SHORTCUT &&
          (event.metaKey || event.ctrlKey)
        ) {
          event.preventDefault()
          toggleSidebar()
        }
      }

      window.addEventListener("keydown", handleKeyDown)
      return () => window.removeEventListener("keydown", handleKeyDown)
    }, [toggleSidebar])

    const state = open ? "expanded" : "collapsed"

    const contextValue = React.useMemo<SidebarContext>(
      () => ({
        state,
        open,
        setOpen,
        isMobile,
        openMobile,
        setOpenMobile,
        toggleSidebar,
        width,
        isResizing,
        handleMouseDown,
      }),
      [
        state,
        open,
        setOpen,
        isMobile,
        openMobile,
        setOpenMobile,
        toggleSidebar,
        width,
        isResizing,
        handleMouseDown,
      ]
    )

    return (
      <SidebarContext.Provider value={contextValue}>
        <TooltipProvider delayDuration={0}>
          <div
            style={
              {
                "--sidebar-width": `${width}px`,
                "--sidebar-width-icon": SIDEBAR_WIDTH_ICON,
                ...style,
              } as React.CSSProperties
            }
            className={cn(
              "group/sidebar-wrapper flex min-h-svh w-full has-[[data-variant=inset]]:bg-sidebar",
              className
            )}
            ref={ref}
            {...props}
          >
            {children}
          </div>
        </TooltipProvider>
      </SidebarContext.Provider>
    )
  }
)
SidebarProvider.displayName = "SidebarProvider"

const Sidebar = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div"> & {
    side?: "left" | "right"
    variant?: "sidebar" | "floating" | "inset"
    collapsible?: "offcanvas" | "icon" | "none"
  }
>(
  (
    {
      side = "left",
      variant = "sidebar",
      collapsible = "offcanvas",
      className,
      children,
      ...props
    },
    ref
  ) => {
    const { isMobile, state, openMobile, setOpenMobile } = useSidebar()

    if (collapsible === "none") {
      return (
        <div
          className={cn(
            "flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground",
            className
          )}
          ref={ref}
          {...props}
        >
          {children}
        </div>
      )
    }

    if (isMobile) {
      return (
        <Sheet open={openMobile} onOpenChange={setOpenMobile} {...props}>
          <SheetContent
            data-sidebar="sidebar"
            data-mobile="true"
            className="w-[--sidebar-width] bg-sidebar p-0 text-sidebar-foreground [&>button]:hidden"
            style={
              {
                "--sidebar-width": SIDEBAR_WIDTH_MOBILE,
              } as React.CSSProperties
            }
            side={side}
          >
            <div className="flex h-full w-full flex-col">{children}</div>
          </SheetContent>
        </Sheet>
      )
    }

    return (
      <div
        ref={ref}
        className="group peer hidden md:block text-sidebar-foreground"
        data-state={state}
        data-collapsible={state === "collapsed" ? collapsible : ""}
        data-variant={variant}
        data-side={side}
      >
        <div
          className={cn(
            "duration-200 relative h-svh w-[--sidebar-width] bg-transparent transition-[width] ease-linear",
            "group-data-[collapsible=offcanvas]:w-0",
            "group-data-[side=right]:rotate-180",
            variant === "floating" || variant === "inset"
              ? "group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4))]"
              : "group-data-[collapsible=icon]:w-[--sidebar-width-icon]"
          )}
        />
        <div
          className={cn(
            "duration-200 fixed inset-y-0 z-10 hidden h-svh w-[--sidebar-width] transition-[left,right,width] ease-linear md:flex",
            side === "left"
              ? "left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]"
              : "right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]",
            variant === "floating" || variant === "inset"
              ? "p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4)_+2px)]"
              : "group-data-[collapsible=icon]:w-[--sidebar-width-icon] group-data-[side=left]:border-r group-data-[side=right]:border-l",
            className
          )}
          {...props}
        >
          <div
            data-sidebar="sidebar"
            className={cn(
              "flex h-full w-full flex-col overflow-hidden",
              className
            )}
          >
            {children}
          </div>
        </div>
      </div>
    )
  }
)
Sidebar.displayName = "Sidebar"

const SidebarHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("flex items-center p-4", className)}
      {...props}
    />
  )
})
SidebarHeader.displayName = "SidebarHeader"

const SidebarContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("flex-1 overflow-auto", className)}
      {...props}
    />
  )
})
SidebarContent.displayName = "SidebarContent"

const SidebarFooter = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("mt-auto flex items-center p-4", className)}
      {...props}
    />
  )
})
SidebarFooter.displayName = "SidebarFooter"

const SidebarTrigger = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<typeof Button>
>(({ className, onClick, ...props }, ref) => {
  const { toggleSidebar, open, isMobile } = useSidebar()

  if (isMobile) {
    return (
      <Button
        ref={ref}
        data-sidebar="sidebar-trigger"
        variant="ghost"
        size="icon"
        className={cn("h-8 w-8", className)}
        onClick={(event) => {
          onClick?.(event)
          toggleSidebar()
        }}
        {...props}
      >
        <PanelLeft />
        <span className="sr-only">Toggle Sidebar</span>
      </Button>
    )
  }

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          ref={ref}
          data-sidebar="sidebar-trigger"
          variant="ghost"
          size="icon"
          className={cn(
            "h-8 w-8 group-data-[collapsible=icon]/sidebar-wrapper:absolute group-data-[collapsible=icon]/sidebar-wrapper:right-0 group-data-[collapsible=icon]/sidebar-wrapper:top-1/2 group-data-[collapsible=icon]/sidebar-wrapper:-translate-y-1/2 group-data-[collapsible=icon]/sidebar-wrapper:translate-x-1/2",
            className
          )}
          onClick={(event) => {
            onClick?.(event)
            toggleSidebar()
          }}
          {...props}
        >
          <PanelLeft
            className={cn(
              "duration-200 h-5 w-5 ease-linear",
              open && "rotate-180"
            )}
          />
        </Button>
      </TooltipTrigger>
      <TooltipContent
        side="right"
        className="flex items-center gap-2"
        sideOffset={12}
      >
        {open ? "Collapse" : "Expand"}
        <span className="text-xs text-muted-foreground">
          ⌘{SIDEBAR_KEYBOARD_SHORTCUT.toUpperCase()}
        </span>
      </TooltipContent>
    </Tooltip>
  )
})
SidebarTrigger.displayName = "SidebarTrigger"

const SidebarResizer = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { side?: "left" | "right" }
>(({ className, side = "left", ...props }, ref) => {
  const { handleMouseDown } = useSidebar()

  return (
    <div
      ref={ref}
      onMouseDown={handleMouseDown}
      onTouchStart={(e) => handleMouseDown(e as any)}
      className={cn(
        "absolute top-0 z-10 h-full w-1.5 cursor-col-resize touch-none",
        side === "right" ? "left-0" : "right-0",
        className
      )}
      {...props}
    />
  )
})
SidebarResizer.displayName = "SidebarResizer"

const SidebarInset = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "duration-200 transition-[margin] ease-linear group-data-[collapsible=offcanvas]/sidebar-wrapper:md:ml-0 group-data-[collapsible=icon]/sidebar-wrapper:md:ml-[calc(var(--sidebar-width-icon)_+_theme(spacing.4))]",
        "group-data-[side=left]/sidebar-wrapper:md:ml-[--sidebar-width]",
        "group-data-[side=right]/sidebar-wrapper:md:mr-[--sidebar-width]",
        className
      )}
      {...props}
    />
  )
})
SidebarInset.displayName = "SidebarInset"

const sidebarMenuButtonVariants = cva(
  "group/sidebar-button flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-sidebar-foreground/80 no-underline transition-colors duration-100 ease-out hover:bg-sidebar-muted/80",
  {
    variants: {
      variant: {
        default: "",
        active:
          "bg-sidebar-muted text-sidebar-foreground hover:bg-sidebar-muted",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const SidebarMenuMain = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("flex flex-col gap-1 p-2", className)}
      {...props}
    />
  )
})
SidebarMenuMain.displayName = "SidebarMenuMain"

interface SidebarMenuButtonProps
  extends React.ComponentProps<typeof Button>,
    VariantProps<typeof sidebarMenuButtonVariants> {
  asChild?: boolean
  icon?: React.ReactNode
}

const SidebarMenuButton = React.forwardRef<
  HTMLButtonElement,
  SidebarMenuButtonProps
>(
  (
    { className, variant, asChild, icon, children, ...props },
    ref
  ) => {
    const { state } = useSidebar()
    const Comp = asChild ? Slot : Button

    if (state === "collapsed") {
      return (
        <Tooltip>
          <TooltipTrigger asChild>
            <Comp
              ref={ref}
              variant="ghost"
              size="icon"
              className={cn("h-9 w-9", variant === "active" && "bg-sidebar-muted text-sidebar-foreground")}
              {...props}
            >
              {icon}
            </Comp>
          </TooltipTrigger>
          <TooltipContent side="right" sideOffset={12}>
            {children}
          </TooltipContent>
        </Tooltip>
      )
    }

    return (
      <Comp
        ref={ref}
        variant="ghost"
        className={cn(sidebarMenuButtonVariants({ variant, className }))}
        {...props}
      >
        {icon}
        {children}
      </Comp>
    )
  }
)
SidebarMenuButton.displayName = "SidebarMenuButton"

const SidebarMenuSub = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<"div">
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("ml-7 flex flex-col gap-1", className)}
      {...props}
    />
  )
})
SidebarMenuSub.displayName = "SidebarMenuSub"

interface SidebarMenuSubButtonProps
  extends React.ComponentProps<typeof Button>,
    VariantProps<typeof sidebarMenuButtonVariants> {
  asChild?: boolean
}

const SidebarMenuSubButton = React.forwardRef<
  HTMLButtonElement,
  SidebarMenuSubButtonProps
>(({ className, variant, asChild, ...props }, ref) => {
  const Comp = asChild ? Slot : Button
  return (
    <Comp
      ref={ref}
      variant="ghost"
      className={cn(sidebarMenuButtonVariants({ variant, className }))}
      {...props}
    />
  )
})
SidebarMenuSubButton.displayName = "SidebarMenuSubButton"

export {
  SidebarProvider,
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarFooter,
  SidebarTrigger,
  SidebarMenuMain,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarInset,
  useSidebar,
  SidebarResizer,
}
