using Microsoft.Azure;
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Web;

namespace PiUi
{
    public class PiUiUtil
    {
        public static async Task<string> GetTokenForCurrentApplication(string authority, string resource, string scope)
        {
            var authContext = new AuthenticationContext(authority);
            ClientCredential clientCred = new ClientCredential(CloudConfigurationManager.GetSetting("ida:ClientId"),
                        CloudConfigurationManager.GetSetting("ida:ClientSecret"));
            AuthenticationResult result = await authContext.AcquireTokenAsync(resource, clientCred);

            if (result == null)
                throw new InvalidOperationException("Failed to obtain the JWT token");

            return result.AccessToken;
        }

    }
}