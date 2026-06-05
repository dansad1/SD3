import type {
  AccordionCtrl,
} from "./types"

type Props = {
  ctrl: AccordionCtrl
}

export function AccordionView({
  ctrl,
}: Props) {

  return (
    <div className="ui-accordion">

      {ctrl.items.map(
        item => {

          const isOpen =
            ctrl.expanded.has(
              item.key
            )

          return (
            <div
              key={item.key}
              className="ui-accordion-item"
            >

              <button
                type="button"
                className="ui-accordion-header"
                onClick={() =>
                  ctrl.toggle(
                    item.key
                  )
                }
              >

                <span>
                  {item.title}
                </span>

                <span>
                  {isOpen
                    ? "−"
                    : "+"}
                </span>

              </button>

              {isOpen && (

                <div
                  className="ui-accordion-content"
                >

                  {item.content}

                </div>

              )}

            </div>
          )
        }
      )}

    </div>
  )
}