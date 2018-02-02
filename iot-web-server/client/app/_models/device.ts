export interface Device {
    id: string,
    name: string,
    description: string,
    log_directory: string,
    board_type: string,
    created_by: string,
    communication_protocols: any,
    devices: any,
    api_version: number,
    log_level: number
}