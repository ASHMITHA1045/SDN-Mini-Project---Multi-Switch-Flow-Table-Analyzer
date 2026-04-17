from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Store flow stats per switch
flow_data = {}

def _handle_ConnectionUp(event):
    log.info(f"Switch {event.dpid} connected")

    # Dummy rule to create UNUSED flow
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.match = of.ofp_match(in_port=99)
    event.connection.send(msg)


def _handle_PacketIn(event):
    in_port = event.port

    msg = of.ofp_flow_mod()
    msg.match.in_port = in_port
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

    event.connection.send(msg)


def _handle_FlowStatsReceived(event):
    dpid = event.connection.dpid
    flow_data[dpid] = event.stats

    print("\n================ DETAILED INFO (First 3 Rules) ================\n")

    count = 1
    for stat in event.stats[:3]:   # show first 3 flows
        status = "ACTIVE" if stat.packet_count > 0 else "UNUSED"

        action_type = "drop"
        if stat.actions:
            action_type = "forward"

        print(f"Flow #{count}")
        print(f" Switch: s{dpid}")
        print(f" Priority: {stat.priority}")
        print(f" Table: 0")
        print(f" Cookie: {stat.cookie}")
        print(f" Match: {stat.match}")
        print(f" Actions: {action_type}")
        print(f" Packets: {stat.packet_count}")
        print(f" Bytes: {stat.byte_count}")
        print(f" Duration(s): {round(stat.duration_sec, 3)}")
        print(f" Idle Timeout: {stat.idle_timeout}")
        print(f" Hard Timeout: {stat.hard_timeout}")
        print(f" Status: {status}\n")

        count += 1

    _print_summary()


def _print_summary():
    print("\n================ SUMMARY (All Switches) ================\n")

    total_flows = 0
    total_active = 0
    total_unused = 0
    total_packets = 0
    total_bytes = 0

    print("Switch  Total  Active  Unused")

    for dpid, stats in flow_data.items():
        total = len(stats)
        active = sum(1 for s in stats if s.packet_count > 0)
        unused = total - active

        total_flows += total
        total_active += active
        total_unused += unused

        for s in stats:
            total_packets += s.packet_count
            total_bytes += s.byte_count

        print(f"s{dpid}      {total}     {active}       {unused}")

    print("\nTOTAL")
    print(f"Flows: {total_flows}")
    print(f"Active: {total_active}")
    print(f"Unused: {total_unused}")
    print(f"Total packets: {total_packets}")
    print(f"Total bytes: {total_bytes}")

    efficiency = (total_active / total_flows * 100) if total_flows > 0 else 0
    print(f"Rule efficiency: {round(efficiency, 2)}%")


def _request_stats():
    for connection in core.openflow._connections.values():
        connection.send(of.ofp_stats_request(
            body=of.ofp_flow_stats_request()
        ))


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow.addListenerByName("FlowStatsReceived", _handle_FlowStatsReceived)

    from pox.lib.recoco import Timer
    Timer(5, _request_stats, recurring=True)
