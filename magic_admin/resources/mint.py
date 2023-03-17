from magic_admin.resources.base import ResourceComponent


class Mint(ResourceComponent):
    
    v1_start_mint721 = "/v1/admin/nft/mint/721_mint"
    v1_start_mint1155 = "/v1/admin/nft/mint/1155_mint"

    def start_mint721(
        self, 
        contract_id: str, 
        quantity: int, 
        destination_address: str,
    ):
        return self.request(
            'post', 
            self.v1_start_mint721,
            params={
                'contract_id': contract_id,
                'quantity': quantity,
                'destination_address': destination_address,
            }
        )
    
    def start_mint1155(
        self,
        contract_id: str,
        quantity: int,
        token_id: int,
        destination_address:str,
    ): 
        return self.request(
            'post',
            self.v1_start_mint1155,
            params={
                'contract_id': contract_id,
                'quantity': quantity,
                'token_id': token_id, 
                'destination_address': destination_address,
            }
        )
    