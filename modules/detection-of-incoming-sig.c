#include <linux/bpf.h>
#include <linux/filter.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>

struct mac_addr {
    __u8 addr[ETH_ALEN];
};

struct packet {
    struct ethhdr eth;
    struct iphdr ip;
};

struct bpf_map_def SEC("maps") process_map = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(int),
    .value_size = sizeof(struct mac_addr),
    .max_entries = 1024,
};

SEC("tracepoint/sound/snd_soc_jack_report")
int bpf_prog(struct pt_regs *ctx)
{
    struct packet pkt = {};

    bpf_probe_read_user(&pkt, sizeof(pkt), (void *)(unsigned long)PT_REGS_PARM1(ctx));

    if (pkt.eth.h_proto == htons(ETH_P_IP) && pkt.ip.protocol == IPPROTO_UDP) {
        int pid = bpf_get_current_pid_tgid();

        struct mac_addr addr = {};
        bpf_probe_read_user(&addr.addr, sizeof(addr.addr), &pkt.eth.h_source);

        bpf_map_update_elem(&process_map, &pid, &addr, BPF_ANY);

        return 0;
    }

    return 0;
}

char _license[] SEC("license") = "GPL";
