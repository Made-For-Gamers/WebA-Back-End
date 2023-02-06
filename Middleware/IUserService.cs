using Datalayer.Models;
using LanguageExt.Common;
using Microsoft.EntityFrameworkCore;

namespace Middleware
{
    public interface IUserService
    {
        User Login(string email, string password);
        Task<User> RegisterUser(string username, string password, string email);

        string StartResetPassword(string email);

        bool EndPasswordReset(string hash, string email, string newPassword);
    }
}