#include <linux/bpf.h>
#include <linux/ptrace.h>
#include <linux/filter.h>
#include <linux/sched.h>
#include <uapi/linux/resource.h>
#include <uapi/linux/mman.h>

#define MAX_PROCESSES 1024

// Define the BPF hash map to store process CPU usage and fan usage
struct bpf_map_def SEC("maps") cpu_fan_map = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(int),
    .value_size = sizeof(int) * 2, // { cpu_time, fan_usage }
    .max_entries = MAX_PROCESSES,
};

SEC("tracepoint/sched/sched_stat_runtime")
int bpf_prog(struct pt_regs *ctx)
{
    struct task_struct *task;
    u64 pid_tgid = bpf_get_current_pid_tgid();
    int pid = pid_tgid >> 32;
    task = (struct task_struct *) bpf_get_current_task();

    int cpu_usage = task->utime + task->stime;
    int fan_usage = 0;

    // Detect interactions with fan usage
    if (task->flags & PF_WQ_WORKER && task->flags & PF_NOFREEZE) {
        fan_usage = 1;
    }

    // Update the BPF map with the CPU and fan usage of the process
    int *usage = bpf_map_lookup_elem(&cpu_fan_map, &pid);
    if (usage) {
        // If the process already exists in the map, update its usage
        usage[0] += cpu_usage;
        usage[1] |= fan_usage;
    } else {
        // If the process is new, insert it into the map
        int new_usage[2] = { cpu_usage, fan_usage };
        bpf_map_update_elem(&cpu_fan_map, &pid, new_usage, BPF_ANY);
    }

    // Check whether the process is performing too many activities in a short duration
    if (cpu_usage < 10000 && fan_usage && usage && usage[0] < 10000) {
        bpf_printk("Process ID %d is performing too many activities in a short duration\n", pid);
    }

    return 0;
}
